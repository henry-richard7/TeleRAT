import pyttsx3


def text_speaker(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
