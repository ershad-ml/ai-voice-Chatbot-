from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QRadialGradient


class AIOrb(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300)

        # State properties
        self.state = "idle"
        self.base_radius = 120
        self.pulse_radius = self.base_radius
        self.pulse_speed = 0.4
        self.max_radius = 135
        self.min_radius = 120
        self.growing = True

        self.color = QColor(0, 170, 255)  # Blue

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    # ---------- STATE CONTROL ----------
    def set_idle(self):
        self.state = "idle"
        self.color = QColor(0, 170, 255)   # Blue
        self.pulse_speed = 0.4

    def set_listening(self):
        self.state = "listening"
        self.color = QColor(255, 60, 60)   # Red
        self.pulse_speed = 1.2

    def set_speaking(self):
        self.state = "speaking"
        self.color = QColor(60, 255, 120)  # Green
        self.pulse_speed = 0.7

    # ---------- ANIMATION ----------
    def animate(self):
        if self.growing:
            self.pulse_radius += self.pulse_speed
            if self.pulse_radius >= self.max_radius:
                self.growing = False
        else:
            self.pulse_radius -= self.pulse_speed
            if self.pulse_radius <= self.min_radius:
                self.growing = True

        self.update()

    # ---------- DRAW ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() // 2
        cy = self.height() // 2

        gradient = QRadialGradient(cx, cy, self.pulse_radius)
        gradient.setColorAt(0.0, self.color)
        gradient.setColorAt(0.5, QColor(self.color.red(), self.color.green(), self.color.blue(), 150))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            cx - self.pulse_radius,
            cy - self.pulse_radius,
            self.pulse_radius * 2,
            self.pulse_radius * 2
        )
