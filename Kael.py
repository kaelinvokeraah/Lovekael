import os
import tempfile
from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
from playsound import playsound

# Load API Key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")

client = OpenAI(api_key=api_key)

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    """Convert text to Myanmar speech and play it."""
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang="my")
        tts.save(fp.name)
        playsound(fp.name)

print("Kael Voice Mode စတင်ပြီးပါပြီ! 'exit' လို့ ပြောရင် ပိတ်သွားပါမယ်။")

# Voice Loop
while True:
    with mic as source:
        print("နားထောင်နေသည်... ပြောပေးပါ...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="my-MM")
        print(f"သင်ပြောခဲ့သည့် စကား: {command}")

        if command.lower() == "exit":
            speak("Kael Voice Mode ပိတ်သွားပါပြီ။")
            print("Goodbye from Kael!")
            break

        # Send to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Kael, a helpful AI assistant."},
                {"role": "user", "content": command}
            ]
        )

        reply = response.choices[0].message.content
        print(f"Kael: {reply}")
        speak(reply)

    except sr.UnknownValueError:
        print("😅 နားမလည်ပါ၊ ပြန်ပြောပါ။")
    except Exception as e:
        print(f"Error: {e}")
