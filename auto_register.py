import cv2
import os
import time
import numpy as np

DATASET_DIR = "dataset"
CASCADE_PATH = "haarcascade_frontalface_default.xml"
CAPTURE_COUNT = 10

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def register_new_user(frame):
    name = input("Enter new user name: ").strip()
    user_dir = os.path.join(DATASET_DIR, name)
    os.makedirs(user_dir, exist_ok=True)

    count = 0
    print("[INFO] Registering new user. Look at the camera.")

    while count < CAPTURE_COUNT:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100)
        )

        if len(faces) == 1:
            x, y, w, h = faces[0]
            face_img = frame[y:y+h, x:x+w]

            if face_img.size == 0:
                continue

            face_img = cv2.resize(face_img, (250, 250))
            face_img = face_img.astype(np.uint8)

            img_path = os.path.join(user_dir, f"{count}.jpg")
            cv2.imwrite(img_path, face_img)

            count += 1
            print(f"[INFO] Captured {count}/{CAPTURE_COUNT}")
            time.sleep(0.4)

    print("[SUCCESS] User registered. Re-run encoding.")
