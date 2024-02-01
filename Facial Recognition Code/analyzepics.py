import os
import cv2
import face_recognition
import pickle

FACES_FOLDER = r'C:\Users\dhirao\Pictures\Faces'
FACES_FILE = r'C:\Users\dhirao\Pictures\Faces_2.0\known_faces.pkl'
LOG_FILE = r'C:\Users\dhirao\Pictures\found_faces_log.txt'

def load_known_faces():
    if os.path.exists(FACES_FILE):
        with open(FACES_FILE, 'rb') as file:
            return pickle.load(file)
    return {}

def compare_and_store_faces(input_folder):
    known_faces = load_known_faces()
    with open(LOG_FILE, 'a') as log_file:
        for filename in os.listdir(input_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                file_path = os.path.join(input_folder, filename)
                face_image = face_recognition.load_image_file(file_path)
                face_encodings = face_recognition.face_encodings(face_image)
                
                if len(face_encodings) > 0:
                    face_encoding = face_encodings[0]
                    matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
                    for i, match in enumerate(matches):
                        if match:
                            name = list(known_faces.keys())[i]
                            output_file = os.path.join(FACES_FOLDER, f"{name}_{filename}")
                            cv2.imwrite(output_file, face_image)
                            print(f"Face of {name} in {filename} stored as {output_file}")
                            log_file.write(f"Face of {name} found in {filename}\n")

def main():
    if not os.path.exists(FACES_FOLDER):
        os.makedirs(FACES_FOLDER)
        
    input_folder = input("Enter the folder path containing face pictures for comparison: ")
    compare_and_store_faces(input_folder)

if __name__ == "__main__":
    main()
