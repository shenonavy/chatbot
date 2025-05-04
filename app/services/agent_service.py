from core.logger import logging
from orchestrator.state_machine import get_rag_tool, get_search_tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from dto.response import ResponseModel

persistent_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)

def _handle_agent_response(response) -> ResponseModel:
    if 'output' in response and 'intermediate_steps' in response:
        source_type = "unknown"
        intermediate_steps = response['intermediate_steps']

        for action, _ in intermediate_steps:
            if action.tool == "RAG Knowledge Base":
                source_type = "knowledge_base"
                break
            elif action.tool == "DuckDuckGo Search":
                source_type = "web_search"
                break

        response_model = ResponseModel(
            status="success",
            response=response['output'],
            source_type=source_type
        )
        return response_model
    return ResponseModel(status="error", response="No valid response", source_type="unknown")

def run_agent(llm, retriever, prompt_template, question: str):
    rag_tool = get_rag_tool(llm, retriever, question)
    search_tool = get_search_tool()

    tools = [rag_tool, search_tool]

    agent = create_react_agent(
        tools=tools,
        llm=llm,
        prompt=prompt_template.get_agent_prompt(),
    )

    agent_executor = AgentExecutor(tools=tools, agent=agent, memory=persistent_memory, handle_parsing_errors=True, verbose=True, return_intermediate_steps=True)

    response = agent_executor.invoke({"input": question})

    logging.info(f"Final result: {response}")

    return _handle_agent_response(response)