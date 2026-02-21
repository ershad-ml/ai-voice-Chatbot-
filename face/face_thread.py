import cv2
import pickle
import numpy as np
import face_recognition
import os
from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QThread, Signal



class FaceAuthThread(QThread):
    authorized = Signal(str)
    unauthorized = Signal()
    unknown_face = Signal()

    def __init__(self):
        super().__init__()
        self.running = True

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.encodings_path = os.path.join(base_dir, "encodings", "encodings.pkl")

        with open(self.encodings_path, "rb") as f:
            self.data = pickle.load(f)
    def run(self):
        video = cv2.VideoCapture(0)

        stable_hits = 0
        REQUIRED_HITS = 5   # face must match 5 consecutive frames

        while self.running:
            ret, frame = video.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            locations = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, locations)

            if not encodings:
                stable_hits = 0
                continue

            name = "Unknown"

            for encoding in encodings:
                distances = face_recognition.face_distance(
                    self.data["encodings"], encoding
                )

                min_dist = np.min(distances)
                if min_dist < 0.45:
                    idx = np.argmin(distances)
                    name = self.data["names"][idx]
                    break

            stable_hits += 1

            if stable_hits >= REQUIRED_HITS:
                if name == "Unknown":
                    self.unknown_face.emit()
                else:
                    self.authorized.emit(name)
                break

            """ if name != "Unknown":
                stable_hits += 1
            else:
                stable_hits = 0
            if stable_hits >= REQUIRED_HITS:
                self.unknown_face.emit()
                break


            if stable_hits >= REQUIRED_HITS:
                self.authorized.emit(name)
                break """

        video.release()



    def stop(self):
        self.running = False
        self.quit()
        self.wait()
