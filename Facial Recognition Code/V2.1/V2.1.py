import cv2
import face_recognition
import os
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading


class FaceRecognitionSystem:
    def __init__(self, pictures_folder):
        self.pictures_folder = pictures_folder
        self.known_faces = self.load_known_faces(pictures_folder)
        self.unknown_faces_count = 0  # Counter for unknown faces

    def load_known_faces(self, pictures_folder):
        known_faces = {"encodings": [], "names": []}
        for filename in os.listdir(pictures_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image = face_recognition.load_image_file(
                    os.path.join(pictures_folder, filename)
                )
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    known_faces["encodings"].append(face_encodings[0])
                    known_faces["names"].append(filename.split(".")[0])
        return known_faces

    @staticmethod
    def assess_image_quality(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    @staticmethod
    def is_new_face(face_encoding, known_encodings, tolerance=0.6):
        if not known_encodings:
            return True
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        return np.all(distances >= tolerance)

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        scale_factor = 0.5  # Adjust scale factor for processing
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=scale_factor, fy=scale_factor)

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(
                self.known_faces["encodings"], face_encoding, tolerance=0.6
            )
            face_label = "Unknown"

            if any(matches):
                first_match_index = matches.index(True)
                face_label = self.known_faces["names"][first_match_index]
            else:
                # Save new unknown face
                top, right, bottom, left = [
                    v * int(1 / scale_factor) for v in face_location
                ]
                new_face_image = frame[top:bottom, left:right]
                self.unknown_faces_count += 1
                unknown_face_filename = f"Unknown_{self.unknown_faces_count}.jpg"
                cv2.imwrite(
                    os.path.join(self.pictures_folder, unknown_face_filename),
                    new_face_image,
                )
                print(f"Unknown face saved as {unknown_face_filename}")

            # Draw rectangle and label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(
                frame,
                face_label,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0,
                (255, 255, 255),
                1,
            )

        return frame


class CameraFeed:
    def __init__(self, camera_index, pictures_folder):
        self.camera_index = int(camera_index)
        self.pictures_folder = pictures_folder
        self.cap = cv2.VideoCapture(self.camera_index)
        self.fr_system = FaceRecognitionSystem(pictures_folder)

    def start_feed(self):
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}.")
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print(f"Error: Could not read frame from camera {self.camera_index}.")
                break

            processed_frame = self.fr_system.process_frame(frame)
            cv2.imshow(f"Camera {self.camera_index}", processed_frame)

            if cv2.waitKey(1) == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


def start_camera_feed(camera_index, pictures_folder):
    camera_feed = CameraFeed(camera_index, pictures_folder)
    camera_feed.start_feed()


class CameraSelector:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Tk()
        self.root.title("Select Cameras")
        self.num_cameras_input = None
        self.camera_listbox = None
        self.camera_list = []

    def create_ui(self):
        label = ttk.Label(self.root, text="Enter number of connected cameras:")
        label.pack(pady=5)

        self.num_cameras_input = ttk.Entry(self.root)
        self.num_cameras_input.pack(pady=5)

        check_button = ttk.Button(
            self.root, text="Check Cameras", command=self.check_cameras
        )
        check_button.pack(pady=10)

        self.camera_listbox = tk.Listbox(self.root, selectmode="multiple")
        self.camera_listbox.pack(pady=5)

    def check_cameras(self):
        num_cameras = int(self.num_cameras_input.get())
        self.camera_list = self.get_camera_list(num_cameras)
        self.update_camera_listbox()

    def get_camera_list(self, max_cameras):
        camera_list = []
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(f"Camera {i}")
                cap.release()
        return camera_list

    def update_camera_listbox(self):
        self.camera_listbox.delete(0, tk.END)
        for camera in self.camera_list:
            self.camera_listbox.insert(tk.END, camera)

        open_button = ttk.Button(
            self.root, text="Open Selected Cameras", command=self.open_cameras
        )
        open_button.pack(pady=10)

    def open_cameras(self):
        selected_indices = [int(index) for index in self.camera_listbox.curselection()]
        self.root.destroy()
        self.callback(selected_indices)

    def start(self):
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":

    def start_selected_cameras(camera_indices):
        threads = []
        pictures_folder = os.path.abspath(r"./Faces/")

        for index in camera_indices:
            thread = threading.Thread(
                target=start_camera_feed, args=(index, pictures_folder)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    camera_selector = CameraSelector(start_selected_cameras)
    camera_selector.start()
