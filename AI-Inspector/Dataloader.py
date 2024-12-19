from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser


def loader(file_path: str):
    data_loader = GenericLoader.from_filesystem(
        file_path,
        glob="*",
        suffixes=['.py', '.js', '.cpp', '.c', '.java', '.rs', '.ts', '.sc', '.cs', '.js', '.kt', '.rb'],
        parser=LanguageParser(),
    )
    docs = data_loader.load()
    return docs[0].page_content
