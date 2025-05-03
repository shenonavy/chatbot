from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import SystemMessage


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