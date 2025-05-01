from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from models.llm import get_llm
from utils.prompt import get_prompt
from entity.chat_request import ChatRequest
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

@app.post("/api/chatbot")
async def chatbot(req: ChatRequest):
    global history

    question = req.question
    logging.info(f"Question: {question}")

    response_data = {
        "status": "success",
        "response": ""
    }

    try:
        prompt = get_prompt()
        logging.info("Received Prompt Template")

        chain = prompt | llm | parser
        logging.info("Created chain")

        history = history[-4:]

        response = chain.invoke({"history": history, "question": [
            HumanMessage(content=question)
        ]})
        logging.info(f"Response: {response}")

        history.extend([HumanMessage(content=question),
                        AIMessage(content=response)])
        
        response_data["response"] = response
        return response_data
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        response_data["response"] = str(e)
        response_data["status"] = "fail"
        return response_data