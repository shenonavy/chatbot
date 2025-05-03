from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableMap
from dto.response import ResponseModel
from core.logger import logging

def run_rag_chain(llm, retriever, prompt_template, question: str) -> ResponseModel:
    try:
        logging.info(f"Running chat rag chain for question: {question}")

        prompt = prompt_template.get_rag_prompt()
        logging.info("Received Prompt Template")

        qa_chain = create_stuff_documents_chain(llm, prompt)

        rag_chain = RunnableMap({
           "context": lambda x: retriever.get_relevant_documents(x["input"]),
           "input": lambda x: x["input"]
        }) | qa_chain
        logging.info("Initialized retriever")

        response = rag_chain.invoke({"input": question})
        logging.info(f"Response: {response}")

        return ResponseModel(response=response)
    except Exception as e:
        logging.error(f"RAG chain error: {str(e)}")
        return ResponseModel(response=str(e), status="fail")