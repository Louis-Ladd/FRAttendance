import cv2
import face_recognition
import threading
import os
import pickle
import tkinter as tk
from tkinter import simpledialog

# Global variables
FACES_FOLDER = "known_faces"
if not os.path.exists(FACES_FOLDER):
    os.makedirs(FACES_FOLDER)


# Load known faces
def load_known_faces():
    known_faces = {}
    for filename in os.listdir(FACES_FOLDER):
        if filename.endswith(".pkl"):
            with open(os.path.join(FACES_FOLDER, filename), "rb") as file:
                known_faces[filename.split(".")[0]] = pickle.load(file)
    return known_faces


# Save a new face encoding with a name
def save_new_face(face_encoding, name):
    with open(os.path.join(FACES_FOLDER, f"{name}.pkl"), "wb") as file:
        pickle.dump(face_encoding, file)
    print(f"New face encoding saved for {name}")


# Prompt for the name and save the new face
def capture_face(face_encoding):
    name = simpledialog.askstring("Input", "Enter the name of the person:")
    if name:
        save_new_face(face_encoding, name)


# Camera feed class
class CameraFeed:
    def __init__(self, camera_index, known_faces):
        self.camera_index = camera_index
        self.known_faces = known_faces
        self.cap = cv2.VideoCapture(camera_index)
        self.running = True

    # Start the camera feed
    def start_feed(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Process the frame
            self.process_frame(frame)

            cv2.imshow("Camera Feed", frame)
            key = cv2.waitKey(1)
            if key % 256 == 27:  # ESC pressed
                self.running = False

    # Process a frame to detect and label known faces
    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings
        ):
            matches = face_recognition.compare_faces(
                list(self.known_faces.values()), face_encoding
            )
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = list(self.known_faces.keys())[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(
                frame,
                name,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (255, 255, 255),
                1,
            )

            # If face not recognized, capture it
            if name == "Unknown":
                capture_face(face_encoding)


# Stop the camera feed
def stop_camera_feed(camera_feed):
    camera_feed.running = False
    camera_feed.cap.release()
    cv2.destroyAllWindows()


# Main program with GUI
if __name__ == "__main__":
    known_faces = load_known_faces()
    root = tk.Tk()
    root.title("Attendance System")

    camera_index = 0  # Default camera
    camera_feed = CameraFeed(camera_index, known_faces)

    # Start the camera thread
    camera_thread = threading.Thread(target=camera_feed.start_feed)
    camera_thread.start()

    # Button to stop the camera feed
    stop_button = tk.Button(
        root, text="Stop Camera", command=lambda: stop_camera_feed(camera_feed)
    )
    stop_button.pack()

    root.mainloop()
    camera_feed.running = False
    camera_thread.join()
