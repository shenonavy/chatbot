import os
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from models.embedding import embedding_model
from utils.loader import splitters

load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL")

vectorstore = PGVector.from_existing_index(
    collection_name="document_vectors",
    connection_string=CONNECTION_STRING,
    embedding=embedding_model
)

vectorstore.add_documents(splitters)