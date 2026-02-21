from voice_utils import speak, listen, play_wakeup
from chatbot_api import ask_chatbot

def start_voice_chat(user_name):
    play_wakeup()
    speak(f"Hello {user_name}. How can I help you?")

    while True:
        user_text = listen()

        if not user_text:
            continue

        if "exit" in user_text.lower() or "stop" in user_text.lower():
            speak("Okay, goodbye.")
            break

        reply = ask_chatbot(user_text)
        speak(reply)
