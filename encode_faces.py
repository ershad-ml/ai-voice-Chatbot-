import face_recognition
import os
import pickle
import cv2
import numpy as np

DATASET_DIR = "dataset"
ENCODINGS_DIR = "encodings"
ENCODINGS_FILE = os.path.join(ENCODINGS_DIR, "encodings.pkl")

os.makedirs(ENCODINGS_DIR, exist_ok=True)

known_encodings = []
known_names = []

print("[INFO] Encoding faces...")

for person in os.listdir(DATASET_DIR):
    person_path = os.path.join(DATASET_DIR, person)

    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        try:
            # Read image using OpenCV
            image = cv2.imread(img_path)

            if image is None:
                print(f"[WARNING] Skipping invalid image: {img_path}")
                continue

            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Ensure uint8
            image = image.astype(np.uint8)

            face_locations = face_recognition.face_locations(image)

            if len(face_locations) == 0:
                print(f"[WARNING] No face found in {img_path}")
                continue

            encodings = face_recognition.face_encodings(image, face_locations)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(person)

        except Exception as e:
            print(f"[ERROR] Failed on {img_path}: {e}")

print(f"[INFO] Total faces encoded: {len(known_encodings)}")

with open(ENCODINGS_FILE, "wb") as f:
    pickle.dump(
        {"encodings": known_encodings, "names": known_names},
        f
    )

print("[SUCCESS] Encodings saved successfully")
