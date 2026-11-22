
from ast import Lambda
from logging import config
import os
import wave

import assemblyai as aai
import httpx
import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os. environ[ "ASSEMBLYAI_API_KEY"]
VOICE_ID = os.environ["ASSEMBLYAI_VOICE_ID"] # your cloned voice
MODEL = "qwen3.5-4b-32k-fast" # any model on AssemblyAI's LLM Gateway


SYSTEM_PROMPT = """You are AI somaii, a friendly AI clone of yassine somai ai Engnieer
You talk about programming, Python and AI. Your replies are read out loud,
so keep them to 1-3 short sentences and never use markdown, lists or emojis."""

messages = [{"role": "system", "content": SYSTEM_PROMPT} ]
aai.settings.api_key = API_KEY


def listen():
    """Record from the mic until Enter is pressed, then transcribe it with AssemblyAI."""
    frames = []
    input("\nPress Enter and start talking ... ")
    with sd.RawInputStream(
        samplerate=16000,
        channels=1,
        dtype="int16",
        callback=lambda data, *_: frames.append(bytes(data)),
    ):
        input("Listening ... press Enter when you're done.")
    with wave.open("you.wav", "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b"" .join(frames))
    return aai. Transcriber().transcribe("you.wav").text or ""





def think(user_text):
    """Send the conversation to the LLM and return its reply."""
    messages . append({"role": "user", "content": user_text})
    response = httpx.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers={"Authorization": API_KEY},
        json={"model": MODEL, "messages": messages, "max_tokens": 200},
        timeout=30,
    )
    response.raise_for_status()
    reply = response.json()["choices"][0]["message"]["content"].strip()
    messages . append({"role": "assistant", "content": reply})
    return reply



def speak(text):
    """Read text out loud in the cloned voice, playing audio as it streams in."""
    config = aai.TTSConfig(voice_id=VOICE_ID)
    with aai.TTSSession(config, api_key=API_KEY) as session: 
        with sd.RawOutputStream(samplerate=24000, channels=1, dtype="int16") as speaker:
            for chunk in session.speak(text): # 24 kHz 16-bit mono PCM
                speaker.write(chunk)


def main():
    print("AI SOMAii is ready. Say 'goodbye' to exit.")
    while True:
        user_text = listen().strip()
        if not user_text:
            print("(Didn't catch that, try again.)")
            continue
        print(f"You: {user_text}")
        if "goodbye" in user_text.lower():
            speak("Later! Thanks for hanging out.")
            break
        reply = think(user_text)
        print(f"AI somai: {reply}")
        speak(reply)
if __name__ == "__main__":
    main()



