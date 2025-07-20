import readline
import os

import openai
from pathlib import Path
from gtts import gTTS

openai.api_key = os.environ.get("OPENAI_API_KEY")


######################################################
######################################################


# LangChain setup
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain.chains import ConversationChain
from langchain_core.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate

# LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Persistent Memory
history = FileChatMessageHistory(file_path="baymax_memory.json")
memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True,
    chat_memory=history
)

# Prompt with system role
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a friendly robot who acts like my best friend."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# LangChain Conversation
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    input_key="input",
    verbose=False
)

def ask(prompt: str) -> str:
    try:
        return conversation.run(prompt)
    except Exception as e:
        print("[!] LangChain error:", e)
        return "Sorry, I couldn’t generate a response."

######################################################
######################################################


def chatgpt_speak(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    with openai.audio.speech.with_streaming_response.create(
      #model="gpt-4o-mini-tts",
      model="tts-1",
      voice="alloy",
      input= text
    ) as response:
      response.stream_to_file(speech_file_path)

def google_speak(text):
    tts = gTTS(text)
    tts.save("speech.mp3")

def speak(text):
    chatgpt_speak(text)
    os.system("mpg123 speech.mp3 1>/dev/null 2>/dev/null")

def query_input() -> str:
    try:
        return input("> ")
    except (KeyboardInterrupt, EOFError):
        print()
        exit(0)


# === Start interaction ===
while True:
    user_input = query_input()
    reply = ask(user_input)
    print("Baymax:", reply)
    speak(reply)
