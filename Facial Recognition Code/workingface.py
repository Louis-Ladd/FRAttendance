import cv2
import face_recognition
import threading
import os
import pickle
import uuid
import json

FACES_FOLDER = r"Faces"


def recognize_face(face_encoding):
    for folder_name in os.listdir(FACES_FOLDER):
        folder_path = os.path.join(FACES_FOLDER, folder_name)
        if os.path.isdir(folder_path):
            encoding_file = os.path.join(folder_path, "encoding.pkl")
            if os.path.exists(encoding_file):
                with open(encoding_file, "rb") as file:
                    known_encoding = pickle.load(file)
                    result = face_recognition.compare_faces(
                        [known_encoding], face_encoding, tolerance=0.6
                    )
                    if result[0]:
                        # Load metadata from JSON if needed, or return the folder name
                        metadata_file = os.path.join(folder_path, "metadata.json")
                        if os.path.exists(metadata_file):
                            with open(metadata_file, "r") as metadata_file:
                                metadata = json.load(metadata_file)
                                return metadata.get("name", "Unknown")
                        return folder_name
    return "Unknown"


# Function to save a new face
def save_face(face_encoding, frame, top, right, bottom, left):
    face_id = str(uuid.uuid4())
    face_folder = os.path.join(FACES_FOLDER, face_id)
    os.makedirs(face_folder, exist_ok=True)

    # Save encoding
    encoding_file = os.path.join(face_folder, "encoding.pkl")
    with open(encoding_file, "wb") as file:
        pickle.dump(face_encoding, file)

    # Save metadata in JSON
    metadata = {"name": "Unknown", "class": "Unknown", "classTime": "Unknown"}
    json_file = os.path.join(face_folder, "metadata.json")
    with open(json_file, "w") as file:
        json.dump(metadata, file)

    print(f"Face {face_id} added and saved")


# Face detection function
def detect_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        name = recognize_face(face_encoding)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        if name == "Unknown":
            save_face(face_encoding, frame, top, right, bottom, left)


# Camera capture thread
def camera_thread(camera_index):
    video_capture = cv2.VideoCapture(camera_index)

    while True:
        ret, frame = video_capture.read()
        detect_face(frame)
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Main program
if __name__ == "__main__":
    # Ensure the faces folder exists
    os.makedirs(FACES_FOLDER, exist_ok=True)

    # Load known faces from the faces folder
    # load_known_faces()

    # Choose the camera index
    camera_index = int(input("Enter the camera index (default is 0): ") or 0)

    # Start camera thread
    camera_thread = threading.Thread(target=camera_thread, args=(camera_index,))
    camera_thread.start()

    # Keep main thread running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Stop camera thread on Ctrl+C
        camera_thread.join()
