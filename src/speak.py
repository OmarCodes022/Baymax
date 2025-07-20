import os
import readline
from pathlib import Path

import openai
from gtts import gTTS
import pyaudio

#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################

def speak(text: str, stream_on: bool = True):
    try:
        if stream_on:
            stream_speak(text)
        else:
            chatgpt_speak(text)
            os.system("mpg123 speech.mp3 1>/dev/null 2>/dev/null")
    except Exception as e:
        print("[!] chatGPT TTS failed, falling back to Google TTS:", e)
        google_speak(text)
        os.system("mpg123 speech.mp3 1>/dev/null 2>/dev/null")

from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

def stream_speak(text: str):
    try:
        # Request speech from OpenAI
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        # Collect all bytes from stream
        audio_data = b""
        for chunk in response.iter_bytes():
            if chunk:
                audio_data += chunk

        if not audio_data:
            raise ValueError("Received empty audio stream.")

        # Decode with pydub
        audio_file = BytesIO(audio_data)
        audio = AudioSegment.from_file(audio_file, format="mp3")  # OpenAI returns MP3 now by default

        # Play
        play(audio)

    except Exception as e:
        print("[!] OpenAI streaming TTS failed:", e)
        raise e

def chatgpt_speak(text: str):
    """
    Uses OpenAI's TTS to generate speech from text.
    Falls back to Google TTS if it fails.
    """
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)

def google_speak(text: str):
    tts = gTTS(text)
    tts.save("speech.mp3")
