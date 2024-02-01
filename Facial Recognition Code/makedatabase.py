import os
import cv2
import face_recognition
import pickle

FACES_FOLDER = r'C:\Users\dhirao\Pictures\Faces_2.0'
FACES_FILE = os.path.join(FACES_FOLDER, 'known_faces.pkl')

def analyze_and_store_faces(folder_path):
    face_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            name = os.path.splitext(filename)[0]
            file_path = os.path.join(folder_path, filename)
            face_image = face_recognition.load_image_file(file_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            face_data[name] = face_encoding
            print(f"Face of {name} analyzed and stored.")

    with open(FACES_FILE, 'wb') as file:
        pickle.dump(face_data, file)
    print("All faces analyzed and stored in the pickle file.")

def main():
    if not os.path.exists(FACES_FOLDER):
        print("Error: Faces folder not found.")
        return

    analyze_and_store_faces(FACES_FOLDER)

if __name__ == "__main__":
    main()
