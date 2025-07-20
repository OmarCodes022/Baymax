import os
import readline
from pathlib import Path
import openai

# === ENVIRONMENT SETUP ===
openai.api_key = os.getenv("OPENAI_API_KEY")

# === LANGCHAIN SETUP ===
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain.chains import ConversationChain
from langchain_core.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate

#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################

# === LLM Setup ===
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# === Persistent Memory ===
history = FileChatMessageHistory(file_path="baymax_memory.json")
memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True,
    chat_memory=history
)

# === Prompt Template ===
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a friendly robot who acts like my best friend."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# === Conversation Chain ===
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    input_key="input",
    verbose=False
)

def ask(prompt: str) -> str:
    try:
        result = conversation.invoke({"input": prompt})
        return result.get("response", "")  # Extract just the bot's message
    except Exception as e:
        print("[!] LangChain error:", e)
        return "Sorry, I couldn’t generate a response."
