import os
from typing import List, Union
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredFileLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

class KnowledgeBaseTool:
    def __init__(self):
        self.knowledge_base = None
        self.embeddings = None

    def add_to_knowledge_base(self, file_paths: Union[str, List[str]]):
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        all_texts = []

        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            try:
                # Choose the appropriate loader based on file extension
                _, file_extension = os.path.splitext(file_path)
                file_extension = file_extension.lower()

                if file_extension == '.pdf':
                    loader = PyPDFLoader(file_path)
                elif file_extension == '.txt':
                    loader = TextLoader(file_path)
                elif file_extension == '.csv':
                    loader = CSVLoader(file_path)
                elif file_extension in ['.doc', '.docx']:
                    loader = UnstructuredWordDocumentLoader(file_path)
                elif file_extension in ['.ppt', '.pptx']:
                    loader = UnstructuredPowerPointLoader(file_path)
                elif file_extension in ['.xls', '.xlsx']:
                    loader = UnstructuredExcelLoader(file_path)
                elif file_extension == '.html':
                    loader = UnstructuredHTMLLoader(file_path)
                elif file_extension in ['.md', '.markdown']:
                    loader = UnstructuredMarkdownLoader(file_path)
                else:
                    # Use UnstructuredFileLoader for any other file type
                    print(f"Using generic loader for unsupported file type: {file_path}")
                    loader = UnstructuredFileLoader(file_path)

                documents = loader.load()

                # print(f"Loaded {len(documents)} document(s) from {file_path}")

                # if documents:
                #     print(f"First document content from {file_path} (truncated to 500 chars): {documents[0].page_content[:500]}")

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=50,
                    length_function=len,
                    is_separator_regex=False,
                )
                texts = text_splitter.split_documents(documents)

                # print(f"Split into {len(texts)} text chunks from {file_path}")

                # for i, chunk in enumerate(texts[:3]):
                #     print(f"Chunk {i + 1} from {file_path} (truncated to 100 chars): {chunk.page_content[:100]}")

                all_texts.extend(texts)

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

        if not all_texts:
            raise ValueError("No valid content was extracted from any of the provided files.")

        try:
            if self.embeddings is None:
                model_name = "sentence-transformers/all-MiniLM-L6-v2"
                self.embeddings = HuggingFaceEmbeddings(model_name=model_name)

            if self.knowledge_base is None:
                self.knowledge_base = FAISS.from_documents(all_texts, self.embeddings)
            else:
                self.knowledge_base.add_documents(all_texts)

            print(f"Successfully added {len(all_texts)} text chunks to the knowledge base")
            return True
        except Exception as e:
            print(f"Error creating/updating knowledge base: {str(e)}")
            raise
        

    def get_knowledge_base_response(self, query: str) -> str:
        if self.knowledge_base is None:
            return "No knowledge base available."

        try:
            qa = RetrievalQA.from_chain_type(
                llm=Ollama(model="llama2"),
                chain_type="stuff",
                retriever=self.knowledge_base.as_retriever()
            )
            return qa.invoke(query)["result"]
        except Exception as e:
            print(f"Error querying knowledge base: {str(e)}")
            return f"An error occurred while processing your query: {str(e)}"
        
    def run(self, query: str,file_paths: Union[str, List[str]]):
        self.add_to_knowledge_base(file_paths)
        response = self.get_knowledge_base_response(query)
        return response

# Usage example
if __name__ == "__main__":
    db = KnowledgeBaseTool()
    try:
        # Add multiple files of different types, including unsupported types
        # db.add_to_knowledge_base(['file.pdf'])
        
        # Query the knowledge base
        query = 'What is the project description?'
        response = db.run(query, ['../files/computer.pdf'])
        print(f"Query: {query}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")