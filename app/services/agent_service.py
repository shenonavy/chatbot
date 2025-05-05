from core.logger import logging
from orchestrator.state_machine import get_custom_prompt_tool, get_rag_tool, get_search_tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from dto.response import ResponseModel

persistent_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)

def _handle_agent_response(response) -> ResponseModel:
    if 'output' in response and 'intermediate_steps' in response:
        source_type = "unknown"
        intermediate_steps = response.get('intermediate_steps', [])

        if 'output' in response and intermediate_steps:
            last_step = intermediate_steps[-1]
            if isinstance(last_step, (list, tuple)) and len(last_step) >= 1:
                last_action = last_step[0]
                if hasattr(last_action, "tool"):
                    if last_action.tool == "RAG Knowledge Base":
                        source_type = "knowledge_base"
                    elif last_action.tool == "DuckDuckGo Search":
                        source_type = "web_search"
                    elif last_action.tool == "AI Assistant":
                        source_type = "ai_assistant"

        response_model = ResponseModel(
            status="success",
            response=response['output'],
            source_type=source_type
        )
        return response_model
    return ResponseModel(status="error", response="No valid response", source_type="unknown")

def run_agent(llm, parser, retriever, prompt_template, question: str):
    try:
        rag_tool = get_rag_tool(llm, retriever, question)
        search_tool = get_search_tool()
        custom_tool = get_custom_prompt_tool(llm, parser, prompt_template, question)
    
        tools = [rag_tool, search_tool, custom_tool]
    
        agent = create_react_agent(
            tools=tools,
            llm=llm,
            prompt=prompt_template.get_agent_prompt(),
        )
    
        agent_executor = AgentExecutor(tools=tools, agent=agent, memory=persistent_memory, handle_parsing_errors=True, verbose=True, return_intermediate_steps=True, max_iterations=10)
    
        response = agent_executor.invoke({"input": question})
    
        logging.info(f"Final result: {response}")
    
        return _handle_agent_response(response)
    except Exception as e:
        logging.error(f"Agent chain error: {str(e)}")
        return ResponseModel(response=str(e), status="fail")