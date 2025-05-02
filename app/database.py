import os
from dotenv import load_dotenv
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import OpenAIEmbeddings 
from models.embedding import embedding_model
from utils.loader import splitters

load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL")

vectorstoreDoc = PGVector.from_documents(
    documents=splitters,
    collection_name="document_vectors",
    connection_string=CONNECTION_STRING,
    embedding_function=embedding_model
)

vectorstore = PGVector(
    documents=splitters,
    collection_name="document_vectors",
    connection_string=CONNECTION_STRING,
    embedding_function=embedding_model
)