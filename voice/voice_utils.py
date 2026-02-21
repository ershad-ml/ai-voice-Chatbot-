import pyttsx3
import threading
import speech_recognition as sr

_engine = None
_tts_thread = None
_stop_flag = False
_lock = threading.Lock()

_recognizer = sr.Recognizer()


def _speak_worker(text):
    global _engine, _stop_flag

    _engine = pyttsx3.init()
    _engine.setProperty("rate", 165)

    _engine.say(text)
    _engine.startLoop(False)

    while _engine.isBusy():
        if _stop_flag:
            _engine.stop()
            break
        _engine.iterate()

    _engine.endLoop()
    _engine = None


def speak(text):
    global _tts_thread, _stop_flag

    stop_speaking()
    _stop_flag = False

    _tts_thread = threading.Thread(
        target=_speak_worker,
        args=(text,),
        daemon=True
    )
    _tts_thread.start()


def stop_speaking():
    global _stop_flag, _engine

    _stop_flag = True
    if _engine:
        try:
            _engine.stop()
        except Exception:
            pass


def listen(timeout=1, phrase_time_limit=5):
    with sr.Microphone() as source:
        try:
            _recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = _recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            return ""

    try:
        return _recognizer.recognize_google(audio).lower()
    except Exception:
        return ""
