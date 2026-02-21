from PySide6.QtCore import QThread, Signal
from voice.voice_utils import listen, speak, stop_speaking
from chatbot_api import ask_chatbot
import time


class VoiceThread(QThread):
    listening = Signal()
    speaking = Signal()
    idle = Signal()
    text_captured = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = False

    def stop(self):
        self._running = False
        from voice.voice_utils import stop_speaking
        stop_speaking()

    def run(self):
        self._running = True

        while self._running:
            self.listening.emit()

            # short timeout listen → allows stop()
            user_text = listen(timeout=1)

            if not self._running:
                break

            if not user_text:
                continue

            self.text_captured.emit(user_text)

            if user_text in ["stop", "exit", "quit"]:
                speak("Conversation ended.")
                break

            self.speaking.emit()
            reply = ask_chatbot(user_text)

            if not self._running:
                break

            speak(reply)
            self.idle.emit()

            time.sleep(0.3)

        self.idle.emit()
