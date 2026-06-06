import speech_recognition as sr
import pyttsx3

# Voice input
def recognize_speech():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text

        except:
            return "Could not recognize speech"

# Text-to-speech
def speak_text(text):

    engine = pyttsx3.init()

    engine.say(text)

    engine.runAndWait()