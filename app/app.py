from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from data import loader as document_loader
from models.llm import get_llm
from prompts import prompt as prompt_template
from schemas.chat_request import ChatRequest
from data.database import vectorstore
from core.logger import logging
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableMap
import shutil
import uuid
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

TEMP_DIR = "./temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

history = []

llm = get_llm()
logging.info("initialized LLM")

parser = StrOutputParser()
logging.info("initialized output parser")

retriever = vectorstore.as_retriever()
logging.info("initialized retriever")

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
        prompt = prompt_template.get_prompt()
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
    
@app.post("/api/rag")
async def rag(req: ChatRequest):
    question = req.question
    logging.info(f"Question: {question}")

    response_data = {
        "status": "success",
        "response": ""
    }

    try:
        prompt = prompt_template.get_rag_prompt()
        logging.info("Load prompt template")

        qa_chain = create_stuff_documents_chain(llm, prompt)

        rag_chain = RunnableMap({
           "context": lambda x: retriever.get_relevant_documents(x["input"]),
           "input": lambda x: x["input"]
        }) | qa_chain
        logging.info("Initialized retriever")

        response = rag_chain.invoke({"input": question})
        logging.info(f"Response: {response}")

        response_data["response"] = response
        return response_data
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        response_data["response"] = str(e)
        response_data["status"] = "fail"
        return response_data
    
@app.post("/api/upload")
async def upload_file(files: List[UploadFile] = File(...)):
    response_data = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            continue

        unique_filename = f"{uuid.uuid4()}.pdf"
        temp_path = os.path.join(TEMP_DIR, unique_filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            splitters = document_loader.doc_loader(temp_path)
            vectorstore.add_documents(splitters)

            response_data.append({
                "original_filename": file.filename,
                "chunks_count": len(splitters),
            })

        except Exception as e:
            response_data.append({
                "original_filename": file.filename,
                "error": str(e),
            })

        finally:
            os.remove(temp_path)

    return {
        "message": f"{len(files)} file(s) uploaded and processed.",
        "results": response_data
    }