import cv2
import os
import pickle
import face_recognition
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
ENCODINGS_PATH = os.path.join(BASE_DIR, "encodings", "encodings.pkl")

def register_face_runtime(name):
    os.makedirs(DATASET_DIR, exist_ok=True)
    user_dir = os.path.join(DATASET_DIR, name)
    os.makedirs(user_dir, exist_ok=True)

    video = cv2.VideoCapture(0)
    encodings = []

    count = 0
    while count < 10:
        ret, frame = video.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)

        if boxes:
            encoding = face_recognition.face_encodings(rgb, boxes)[0]
            encodings.append(encoding)
            cv2.imwrite(os.path.join(user_dir, f"{count}.jpg"), frame)
            count += 1

    video.release()

    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)

    for enc in encodings:
        data["encodings"].append(enc)
        data["names"].append(name)

    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)
