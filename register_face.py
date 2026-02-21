import cv2
import os
import time
import numpy as np

DATASET_DIR = "dataset"
CAPTURE_COUNT = 10
CASCADE_PATH = "haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

name = input("Enter new user name: ").strip()
user_dir = os.path.join(DATASET_DIR, name)
os.makedirs(user_dir, exist_ok=True)

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video.isOpened():
    print("[ERROR] Camera not accessible")
    exit()

count = 0
print("[INFO] Capturing face images. Please look at the camera.")

def register_new_face(self, name, frame):
    import os
    import cv2
    import time
    import subprocess

    base_dir = self.get_data_dir()
    user_dir = os.path.join(base_dir, "dataset", name)
    os.makedirs(user_dir, exist_ok=True)

    count = 0
    cap = cv2.VideoCapture(0)

    while count < 10:
        ret, img = cap.read()
        if not ret:
            continue

        cv2.imwrite(
            os.path.join(user_dir, f"{count}.jpg"),
            img
        )
        count += 1
        time.sleep(0.2)

    cap.release()

    # Re-encode faces
    self.reencode_faces()

    # Reload encodings in FaceThread
    self.face_thread.reload_encodings()


while count < CAPTURE_COUNT:
    ret, frame = video.read()
    if not ret or frame is None:
        continue

    frame = frame.astype(np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    if len(faces) == 1:
        x, y, w, h = faces[0]
        face_img = frame[y:y+h, x:x+w]

        if face_img.size == 0:
            continue

        face_img = cv2.resize(face_img, (250, 250))
        img_path = os.path.join(user_dir, f"{count}.jpg")
        cv2.imwrite(img_path, face_img)

        count += 1
        print(f"[INFO] Captured {count}/{CAPTURE_COUNT}")
        time.sleep(0.5)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Register Face", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()

print("[SUCCESS] Face registered correctly. Now run encode_faces.py")
