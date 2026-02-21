import subprocess

print("1. Recognize Face")
print("2. Register New Face")

choice = input("Choose option: ")

if choice == "1":
    subprocess.run(["python", "recognize_face.py"])
elif choice == "2":
    subprocess.run(["python", "register_face.py"])
    subprocess.run(["python", "encode_faces.py"])
else:
    print("Invalid choice")
