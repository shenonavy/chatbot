from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from dto.response import ResponseModel
from models.llm import get_llm
from data.database import vectorstore
from core.logger import logging
from routers import chatbot, upload
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Chatbot",
    version="1.0",
    description="A simple chatbot API"
)
logging.info("initialized FastAPI server")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.llm = get_llm()
logging.info("initialized LLM")

app.state.parser = StrOutputParser()
logging.info("initialized output parser")

app.state.retriever = vectorstore.as_retriever()
logging.info("initialized retriever")

app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])

@app.get("/")
async def index():
    return ResponseModel(status="success", response="Welcome to Chatbot API")