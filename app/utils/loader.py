from langchain_community.document_loaders import PyPDFLoader
from utils.document_splitter import splitter

def doc_loader(path: str):
    loader = PyPDFLoader(path)
    docs = loader.load()
    splitters = splitter(docs)
    return splitters