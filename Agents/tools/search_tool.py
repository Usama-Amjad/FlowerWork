import requests
from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urlparse, quote
from typing import List, Dict, Optional
import time
import random

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebSearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def _is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        return text

    def _perform_search(self, query: str, num_results: int, max_retries: int = 3) -> List[Dict[str, str]]:
        encoded_query = quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Sending request to URL: {url} (Attempt {attempt + 1})")
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 202:
                    logger.debug(f"Received 202 status code. Retrying in 5 seconds...")
                    time.sleep(5)
                    continue
                
                response.raise_for_status()
                logger.debug(f"Response status code: {response.status_code}")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                logger.debug(f"HTML content length: {len(response.text)}")
                
                results = soup.find_all('div', class_='result')
                logger.debug(f"Found {len(results)} result divs")
                
                search_results = []
                for result in results[:num_results]:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        url = title_elem['href']
                        if self._is_valid_url(url):
                            search_results.append({
                                'title': title_elem.text.strip(),
                                'url': url,
                                'snippet': snippet_elem.text.strip()
                            })
                
                logger.debug(f"Processed {len(search_results)} valid results")
                return search_results
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (Attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("Max retries reached. Giving up.")
                    return []
                time.sleep(5)
        
        return []

    def search_web(self, 
                  query: str, 
                  num_results: int = 5, 
                  extract_content: bool = True) -> List[Dict[str, str]]:
        try:
            results = self._perform_search(query, num_results)
            
            if extract_content and results:
                for result in results:
                    try:
                        content = self._extract_page_content(result['url'])
                        if content:
                            result['content'] = content
                        time.sleep(random.uniform(1.0, 2.0))
                    except Exception as e:
                        logger.error(f"Error extracting content from {result['url']}: {str(e)}")
            
            return results
        
        except Exception as e:
            logger.error(f"Search failed: {str(e)}", exc_info=True)
            return []

    def _extract_page_content(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'iframe']):
                element.decompose()
            
            content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
            content = ' '.join([tag.get_text() for tag in content_tags])
            
            return self._clean_text(content)[:5000]
        
        except Exception as e:
            logger.error(f"Content extraction failed for {url}: {str(e)}")
            return None

    @staticmethod
    def format_results(results: List[Dict[str, str]]) -> str:
        if not results:
            return "No results found."
        
        formatted_results = []
        for idx, result in enumerate(results, 1):
            formatted_result = f"{idx}. {result['title']}\n   URL: {result['url']}\n   Snippet: {result['snippet']}"
            if 'content' in result:
                formatted_result += f"\n   Content: {result['content'][:200]}..."
            formatted_results.append(formatted_result)
        
        return "\n\n".join(formatted_results)

    def search_and_process(self, query: str) -> str:
        logger.info(f"Starting search for query: {query}")
        results = self.search_web(query, 4, True)
        return self.format_results(results)

# Main execution
if __name__ == "__main__":
    query = "latest developments in renewable energy"
    print(f"Searching for: {query}\n")
    
    try:
        searcher = WebSearcher()
        results = searcher.search_and_process(query)
        print(results)
    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}", exc_info=True)