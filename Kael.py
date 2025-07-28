import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key
load_dotenv()
api_key = os.getenv("")
client = OpenAI(api_key=api_key)

recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang="my")
        tts.save(fp.name)
        playsound(fp.name)

print("Kael Voice Mode စလို့ပြီးပါပြီ! 'exit' ဆိုရင် ပိတ်မယ်။")

while True:
    with mic as source:
        print("ပြောပါ...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language="my-MM")
        print("You:", user_input)

        if user_input.lower() == "exit":
            speak("ပြန်တွေ့မယ်နော်")
            break

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Kael, a helpful Burmese-speaking AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        kael_reply = response.choices[0].message.content
        print("Kael:", kael_reply)
        speak(kael_reply)

    except Exception as e:
        print("Error:", e)
        speak("နားမလည်ပါ")
