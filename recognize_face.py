import cv2
import face_recognition
import pickle
import numpy as np
import os
import time
import sys
import subprocess
from auto_register import register_new_user
from voice_chatbot import start_voice_chat


# ---------------- CONFIG ----------------
ENCODINGS_FILE = os.path.join("encodings", "encodings.pkl")
CASCADE_PATH = "haarcascade_frontalface_default.xml"

access_granted = False

DISTANCE_THRESHOLD = 0.6        # correct threshold for face_recognition
PROCESS_EVERY_N_FRAMES = 5
PROMPT_COOLDOWN_SECONDS = 3
# ---------------------------------------

# Load encodings
with open(ENCODINGS_FILE, "rb") as f:
    data = pickle.load(f)

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# State variables
frame_count = 0
unknown_prompted = False
ignore_unknown = False
last_prompt_time = 0

print("[INFO] Face recognition with auto-registration started")

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_count += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ---------- FACE DETECTION (FAST) ----------
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(60, 60)
    )

    # Reset state when no face
    if len(faces) == 0:
        unknown_prompted = False
        ignore_unknown = False

    for (x, y, w, h) in faces:
        # Draw detection box immediately (yellow)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    # ---------- RECOGNITION (EVERY N FRAMES) ----------
    if frame_count % PROCESS_EVERY_N_FRAMES == 0:
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (150, 150))
            rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

            encodings = face_recognition.face_encodings(rgb)
            if not encodings:
                continue

            encoding = encodings[0]
            distances = face_recognition.face_distance(data["encodings"], encoding)

            name = "Unknown"

            if len(distances) > 0:
                min_dist = np.min(distances)
                index = np.argmin(distances)

                if min_dist <= DISTANCE_THRESHOLD:
                    name = data["names"][index]
                    access_granted = True
                    unknown_prompted = False
                    ignore_unknown = False
                    start_voice_chat(name)
                    break

            # Draw recognition result
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame,
                name,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2
            )
            if access_granted:
                cv2.putText(
                frame,
                "         ACCESS GRANTED",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
                )


            # ---------- AUTO REGISTER UNKNOWN ----------
            current_time = time.time()

            if name == "Unknown" and not ignore_unknown:
                if (not unknown_prompted and
                    current_time - last_prompt_time > PROMPT_COOLDOWN_SECONDS):

                    unknown_prompted = True
                    last_prompt_time = current_time

                    print("\n[INFO] Unknown face detected.")
                    choice = input("Register new user? (y/n): ").lower()

                    if choice == "y":
                        register_new_user(frame)
                        print("[INFO] Updating encodings...")
                        subprocess.run([sys.executable, "encode_faces.py"])
                        print("[INFO] Restart the application.")
                        video.release()
                        cv2.destroyAllWindows()
                        exit()
                    else:
                        print("[INFO] Registration skipped.")
                        ignore_unknown = True

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
