import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ai_orb import AIOrb
from voice.voice_thread import VoiceThread
from face.face_thread import FaceAuthThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print("MainWindow started")

        self.setWindowTitle("AI Assistant")
        self.showFullScreen()
        # set image background (falls back to black if image not found)
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "background.jpg"))
        if os.path.exists(img_path):
            img_url = img_path.replace("\\", "/")
            self.setStyleSheet(f"""
            QMainWindow {{
                background-image: url("{img_url}");
                background-repeat: no-repeat;
                background-position: center;
            }}
            """)
        else:
            self.setStyleSheet("background-color: black;")

        # ---------- CENTRAL ----------
        central = QWidget()
        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # ---------- TOP BAR ----------
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(36, 36)
        self.close_btn.setStyleSheet("""
            QPushButton {
                color: red;
                font-size: 18px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #330000;
                border-radius: 18px;
            }
        """)
        self.close_btn.clicked.connect(self.close)

        top_bar.addWidget(self.close_btn)
        self.main_layout.addLayout(top_bar)

        # ---------- ORB ----------
        self.orb = AIOrb()
        self.main_layout.addWidget(self.orb, alignment=Qt.AlignCenter)

        # ---------- STATUS ----------
        self.status = QLabel("Scanning face...")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont("Segoe UI", 16))
        self.status.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.status)

        # ---------- CHAT ----------
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("border: none;")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(12)

        self.chat_area.setWidget(self.chat_container)
        self.chat_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.chat_area)

        # ---------- INPUT BAR ----------
        input_container = QWidget()
        input_container.setFixedHeight(60)
        input_container.setFixedWidth(700)
        input_container.setStyleSheet("""
            QWidget {
                background-color: #0e0e0e;
                border-radius: 30px;
                border: 2px solid #b02020;
            }
        """)

        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(20, 0, 15, 0)
        input_layout.setSpacing(15)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Ask me anything...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: white;
                font-size: 16px;
            }
        """)

        self.voice_btn = QPushButton("🎤")
        self.voice_btn.setFixedSize(36, 36)

        self.stop_btn = QPushButton("■")
        self.stop_btn.setFixedSize(36, 36)

        self.send_btn = QPushButton("➤")
        self.send_btn.setFixedSize(36, 36)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #b02020;
                color: white;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: #d03030;
            }
        """)

        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.voice_btn)
        input_layout.addWidget(self.stop_btn)
        input_layout.addWidget(self.send_btn)

        self.main_layout.addWidget(input_container, alignment=Qt.AlignCenter)

        # ---------- DISABLE INPUT INITIALLY ----------
        self.text_input.setEnabled(False)
        self.send_btn.setEnabled(False)
        self.voice_btn.setEnabled(False)

        # ---------- FACE AUTH ----------
        self.face_thread = FaceAuthThread()
        self.face_thread.authorized.connect(self.on_face_authorized)
        self.face_thread.unauthorized.connect(self.on_face_unauthorized)
        self.face_thread.start()

        self.face_thread.unknown_face.connect(self.on_unknown_face)


        self.orb.set_listening()

        # ---------- VOICE THREAD ----------
        self.voice_thread = None

        # ---------- SIGNALS ----------
        self.send_btn.clicked.connect(self.on_text_send)
        self.text_input.returnPressed.connect(self.on_text_send)
        self.voice_btn.clicked.connect(self.on_voice_start)
        self.stop_btn.clicked.connect(self.on_stop)

    def on_unknown_face(self):
        from PySide6.QtWidgets import QInputDialog, QMessageBox

        name, ok = QInputDialog.getText(
            self,
            "New Face Detected",
            "Enter your name to register:"
        )

        if not ok or not name.strip():
            QMessageBox.warning(self, "Cancelled", "Face not registered.")
            return

        self.status.setText("Registering face...")
        self.orb.set_listening()

        from face.register_runtime import register_face_runtime
        register_face_runtime(name.strip())

        QMessageBox.information(
            self,
            "Success",
            f"Face registered for {name}"
        )

        self.status.setText(f"Welcome, {name}")
        self.orb.set_idle()

        self.text_input.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.voice_btn.setEnabled(True)
                        

    # ---------- CHAT ----------
    def add_message(self, text, sender="ai"):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(520)
        bubble.setStyleSheet("""
            QLabel {
                padding: 10px 14px;
                border-radius: 12px;
                color: white;
                font-size: 14px;
            }
        """)

        row = QHBoxLayout()
        if sender == "user":
            bubble.setStyleSheet(bubble.styleSheet() + "background:#007acc;")
            row.addStretch()
            row.addWidget(bubble)
        else:
            bubble.setStyleSheet(bubble.styleSheet() + "background:#2a2a2a;")
            row.addWidget(bubble)
            row.addStretch()

        container = QWidget()
        container.setLayout(row)
        self.chat_layout.addWidget(container)

        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )

    # ---------- FACE CALLBACKS ----------
    def on_face_authorized(self, name):
        self.status.setText(f"Welcome, {name}")
        self.orb.set_idle()

        self.text_input.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.voice_btn.setEnabled(True)

    def on_face_unauthorized(self):
        self.status.setText("Face not recognized")
        self.orb.set_idle()

    # ---------- STATES ----------
    def set_idle(self):
        self.status.setText("Idle")
        self.orb.set_idle()

    def set_listening(self):
        self.status.setText("Listening...")
        self.orb.set_listening()

    def set_speaking(self):
        self.status.setText("Speaking...")
        self.orb.set_speaking()

    # ---------- TEXT ----------
    def on_text_send(self):
        text = self.text_input.text().strip()
        if not text:
            return

        self.text_input.clear()
        self.add_message(text, "user")
        self.set_speaking()

        from chatbot_api import ask_chatbot
        response = ask_chatbot(text)

        self.add_message(response, "ai")

        from voice.voice_utils import speak
        speak(response)

        self.set_idle()

    # ---------- VOICE ----------
    def on_voice_start(self):
        if self.voice_thread and self.voice_thread.isRunning():
            return

        self.voice_thread = VoiceThread()
        self.voice_thread.listening.connect(self.set_listening)
        self.voice_thread.speaking.connect(self.set_speaking)
        self.voice_thread.idle.connect(self.set_idle)
        self.voice_thread.text_captured.connect(
            lambda text: self.add_message(text, "user")
        )
        self.voice_thread.start()

    # ---------- STOP ----------
    def on_stop(self):
        if self.voice_thread and self.voice_thread.isRunning():
            self.voice_thread.stop()

        from voice.voice_utils import stop_speaking
        stop_speaking()

        self.set_idle()

    # ---------- CLEAN EXIT ----------
    def closeEvent(self, event):
        if self.voice_thread and self.voice_thread.isRunning():
            self.voice_thread.stop()
        event.accept()


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
