from langchain_community.document_loaders import PyPDFLoader
from utils.document_splitter import splitter

loader = PyPDFLoader("./docs/btg.pdf")

docs = loader.load()

splitters = splitter(docs)