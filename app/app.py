from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from models.llm import get_llm
from logger import logging
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Chatbot",
    version="1.0",
    description="A simple chatbot API"
)
logging.info("initialized FastAPI server")

history = []

llm = get_llm()
logging.info("initialized LLM")

parser = StrOutputParser()
logging.info("initialized output parser")

@app.get("/")
async def index():
    response_data = {
        "status": "success",
        "response": "Welcome to Chatbot"
    }
    return response_data