from langchain_core.messages import HumanMessage, AIMessage
from dto.response import ResponseModel
from core.logger import logging

history = []

def run_chatbot_chain(llm, parser, prompt_template, question: str) -> ResponseModel:
    global history

    try:
        logging.info(f"Running chat chain for question: {question}")

        prompt = prompt_template.get_prompt()
        logging.info("Received Prompt Template")

        chain = prompt |  llm |  parser
        logging.info("Created chain")

        history = history[-4:]

        response = chain.invoke({"history": history, "question": [
            HumanMessage(content=question)
        ]})
        logging.info(f"Response: {response}")

        history.extend([HumanMessage(content=question),
                        AIMessage(content=response)])
        
        return ResponseModel(response=response)
    except Exception as e:
        logging.error(f"Chat chain error: {str(e)}")
        return ResponseModel(response=str(e), status="fail")