from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate


def get_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="You are an intelligent chatbot. Answer the following question."),
            MessagesPlaceholder(variable_name="history"),
            MessagesPlaceholder(variable_name="question")
        ]
    )
    return prompt

def get_rag_prompt():
    system_prompt = (
        "You are an intelligent chatbot. Use the following context to answer the question. If you don't know the answer, just say that you don't know."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    return prompt

def get_agent_prompt():
    template= '''
          Answer the following questions as best you can. You have access to the following tools:

          {tools}

          Use the following format:

          Question: the input question you must answer
          Thought: you should always prefer using the RAG Knowledge Base tool first. If it doesn't give a satisfactory answer (e.g., "I don't know"), proceed to the next tool.
          Action: the action to take, should be one of [{tool_names}]. Always look first in Vector Store
          Action Input: the input to the action
          Observation: the result of the action
          ... (this Thought/Action/Action Input/Observation can repeat 2 times)
          Thought: I now know the final answer
          Final Answer: the final answer to the original input question

          Begin!

          Question: {input}
          Thought:{agent_scratchpad}
          '''
    prompt = PromptTemplate.from_template(template)
    return prompt