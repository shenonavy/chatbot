from xml.dom.minidom import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def splitter(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    return splits