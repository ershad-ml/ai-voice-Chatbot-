# 🤖 AI Voice Assistant with Face Recognition (Offline LLM)

## 📌 Project Overview

This project is a desktop-based AI Assistant that integrates:

-   🧠 Local Large Language Model (LLM) via Ollama\
-   🎤 Voice input & speech output\
-   📷 Real-time face recognition\
-   🖥 Modern GUI using PySide6

The system runs fully offline using a locally hosted model (`gemma:2b`)
without any cloud APIs.

------------------------------------------------------------------------

## 🚀 Key Features

-   💬 GPT-style conversational chatbot
-   🧠 Local AI inference using Ollama
-   🎙 Speech-to-text (microphone input)
-   🔊 Text-to-speech response
-   👤 Face recognition authentication
-   🖼 GUI-based desktop interface
-   ⚡ GPU acceleration support (if available)

------------------------------------------------------------------------

## 🏗 Project Structure

AI-ML-Chatbot/ │ ├── ui/ │ └── main_window.py \# Main GUI entry point │
├── face/ │ ├── face_thread.py │ └── register_runtime.py │ ├── voice/ │
├── voice_thread.py │ └── voice_utils.py │ ├── chatbot/ │ ├── encodings/
│ └── encodings.pkl \# Pre-generated face encodings │ ├── chatbot_api.py
\# Ollama API integration ├── encode_faces.py \# Generate face encodings
├── recognize_face.py ├── register_face.py ├── auto_register.py ├──
AI_Assistant.spec \# PyInstaller build config ├── requirements.txt └──
README.md

------------------------------------------------------------------------

## 🧠 AI Model Details

This project uses:

-   Ollama for local model hosting
-   Model: `gemma:2b`

Advantages: - No API key required - No internet required after setup -
Fully offline inference - Faster demo performance on CPU systems

------------------------------------------------------------------------

## ⚙️ Installation (Source Code Version)

### 1️⃣ Install Python (3.10 recommended)

### 2️⃣ Install Dependencies

pip install -r requirements.txt

> ⚠ On Windows, `dlib` and `PyAudio` may require precompiled wheels.

------------------------------------------------------------------------

### 3️⃣ Install Ollama

Download from: https://ollama.com

------------------------------------------------------------------------

### 4️⃣ Download Model

ollama pull gemma:2b

------------------------------------------------------------------------

### 5️⃣ Run Application

python ui/main_window.py

------------------------------------------------------------------------

## 📦 Running EXE Version (College Demo)

If using the compiled `.exe`:

1.  Install Ollama\
2.  Run: ollama pull gemma:2b\
3.  Ensure Ollama is running\
4.  Double-click `AI_Assistant.exe`\
5.  Allow microphone and camera permissions

------------------------------------------------------------------------

## 🖥 Hardware Requirements

Minimum (Tested on):

-   Intel i5
-   16GB RAM
-   Windows 10/11
-   Webcam & Microphone

Recommended:

-   GPU (NVIDIA RTX series)
-   16GB+ RAM

------------------------------------------------------------------------

## 🔧 Technologies Used

-   Python
-   PySide6 (GUI)
-   OpenCV
-   dlib
-   face-recognition
-   SpeechRecognition
-   PyAudio
-   pyttsx3
-   Ollama (Local LLM runtime)

------------------------------------------------------------------------

## 🎓 Academic Purpose

This project demonstrates:

-   Integration of computer vision and NLP
-   Local LLM deployment
-   Real-time face authentication
-   Voice-based AI interaction
-   Desktop application packaging using PyInstaller

------------------------------------------------------------------------

## 📌 Notes

-   Encodings are pre-generated (`encodings.pkl`)
-   If dataset changes, run:

python encode_faces.py

to regenerate encodings.

------------------------------------------------------------------------

## 👨‍💻 Author

Faiz\
AI/ML Project -- Academic Submission
