from core.logger import logging
from langchain.agents import Tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun

history = []

def get_rag_tool(llm, retriever, question: str):
    logging.info(f"Running chat rag chain for question: {question}")

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
    )

    return Tool(
        name="RAG Knowledge Base",
        func=rag_chain.run,
        description="Use this tool to answer questions using the internal knowledge base documents."
    )

def get_search_tool():
    return Tool(
        name="DuckDuckGo Search",
        func=_safe_duckduckgo_search,
        description=(
            "Use this tool to search the web for up-to-date or general knowledge questions. "
            "Good for news, live data, or unknown topics."
        )
    )

def get_custom_prompt_tool(llm, parser, prompt_template, question: str):
    global history

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
    
    def custom_tool_func(q: str):
        return response
    
    return Tool(
        name="AI Assistant",
        func=custom_tool_func,
        description="Use this tool to search the AI assistant."  
    )

def _safe_duckduckgo_search(query: str) -> str:
    try:
        return DuckDuckGoSearchRun().run(query)
    except Exception as e:
        logging.warning(f"DuckDuckGo search failed: {str(e)}")
        return "I'm not sure about that. Please try again later or rephrase your question."