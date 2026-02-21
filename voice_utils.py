import pyttsx3
import speech_recognition as sr
import winsound
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 165)

def play_wakeup():
    # Beep sound (frequency, duration)
    winsound.Beep(1200, 300)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text
    except:
        return ""


def listen(timeout=5, phrase_time_limit=7):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text

    except sr.UnknownValueError:
        print("[Could not understand audio]")
        return ""

    except sr.RequestError as e:
        print("[STT API error]", e)
        return ""
