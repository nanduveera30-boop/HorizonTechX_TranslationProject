import speech_recognition as sr

# Voice input
def recognize_speech():
    try:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            print("Listening...")

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            return text

    except Exception:
        return "Voice input is not available in cloud deployment."

# Text-to-speech
def speak_text(text):
    # Disabled for Streamlit Cloud deployment
    return