import readline
import os

import openai
from pathlib import Path
from gtts import gTTS

openai.api_key = os.environ.get("OPENAI_API_KEY")

# LANGCHAIN
import getpass
import os

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")
model.invoke("Hello, world!")
######################################################


def ask(prompt):
    try:
        response = openai.chat.completions.create(
            #model="gpt-4o",
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly robot who acts like my best friend."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("[!] Error from OpenAI:", e)
        return "Sorry, I couldn't think of a reply. My brain needs charging."


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
