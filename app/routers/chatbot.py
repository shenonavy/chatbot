from fastapi import APIRouter, Request
from services.chatbot_service import run_chatbot_chain
from services.rag_service import run_rag_chain
from schemas.chat_request import ChatRequest
from prompts import prompt as prompt_template

router = APIRouter()

@router.post("/chatbot")
async def chatbot(req: ChatRequest, request: Request):
    response_model = run_chatbot_chain(
        llm=request.app.state.llm,
        parser=request.app.state.parser,
        prompt_template=prompt_template,
        question=req.question
    )
    return response_model

@router.post("/rag")
async def rag(req: ChatRequest, request: Request):
    response_model = run_rag_chain(
        llm=request.app.state.llm,
        retriever=request.app.state.retriever,
        prompt_template=prompt_template,
        question=req.question
    )
    return response_model