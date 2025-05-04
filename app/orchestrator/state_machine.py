from core.logger import logging
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun

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

def _safe_duckduckgo_search(query: str) -> str:
    try:
        return DuckDuckGoSearchRun().run(query)
    except Exception as e:
        logging.warning(f"DuckDuckGo search failed: {str(e)}")
        return "I'm not sure about that. Please try again later or rephrase your question."