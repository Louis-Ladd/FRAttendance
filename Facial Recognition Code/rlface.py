import cv2
import dlib
import face_recognition
import os
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading

class FaceRecognitionSystem:
    def __init__(self, base_folder):
        self.base_folder = base_folder
        self.known_faces = self.load_known_faces(base_folder)

    def load_known_faces(self, base_folder):
        known_faces = {"encodings": [], "names": []}
        for root, dirs, files in os.walk(base_folder):
            for filename in files:
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    image_path = os.path.join(root, filename)
                    label, angle = self.extract_label_and_angle(image_path)
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        known_faces["encodings"].append(face_encodings[0])
                        known_faces["names"].append((label, angle))
        return known_faces

    @staticmethod
    def extract_label_and_angle(image_path):
        filename = os.path.basename(image_path)
        parts = filename.split("_")
        label = parts[0]
        angle = parts[1].split(".")[0] if len(parts) > 1 else "front"
        return label, angle

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
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Find face locations using Dlib
        face_locations = face_recognition.face_locations(small_frame, model="cnn")
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            top, right, bottom, left = [v * 4 for v in face_location]
            face_image = frame[top:bottom, left:right]
            image_quality = self.assess_image_quality(face_image)

            matches = face_recognition.compare_faces(
                self.known_faces["encodings"], face_encoding, tolerance=0.6
            )
            label, angle = "Unknown", "front"

            if any(matches):
                first_match_index = matches.index(True)
                label, angle = self.known_faces["names"][first_match_index]

                old_image_path = os.path.join(
                    self.base_folder, label, f"{label}_{angle}.jpg"
                )
                if os.path.exists(old_image_path):
                    old_image = cv2.imread(old_image_path)
                    old_image_quality = self.assess_image_quality(old_image)

                    if image_quality > old_image_quality:
                        cv2.imwrite(old_image_path, face_image)
                        print(
                            f"Updated image for {label} with a better quality image (Angle: {angle})."
                        )
            elif self.is_new_face(face_encoding, self.known_faces["encodings"]):
                label, angle = f"face_{len(self.known_faces['encodings']) + 1}", "front"
                self.known_faces["encodings"].append(face_encoding)
                self.known_faces["names"].append((label, angle))
                folder_path = os.path.join(self.base_folder, label)
                os.makedirs(folder_path, exist_ok=True)
                cv2.imwrite(
                    os.path.join(folder_path, f"{label}_{angle}.jpg"), face_image
                )
                print(f"New face detected and saved as {label} (Angle: {angle})")

            # Draw rectangle and label on the frame
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label} ({angle})",
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0,
                (255, 255, 255),
                1,
            )


class CameraFeed:
    def __init__(self, camera_index, base_folder):
        self.camera_index = camera_index
        self.base_folder = base_folder
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.fr_system = FaceRecognitionSystem(base_folder)
        self.face_tracker = dlib.correlation_tracker()

    def start_feed(self):
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}.")
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print(
                    f"Error: Could not read frame from camera {self.camera_index}."
                )
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            face_locations = face_recognition.face_locations(small_frame, model="cnn")

            if face_locations:
                top, right, bottom, left = face_locations[0]
                self.face_tracker.start_track(
                    small_frame, dlib.rectangle(left, top, right, bottom)
                )
                face_rect = self.face_tracker.get_position()
                left, top, right, bottom = (
                    int(face_rect.left() * 4),
                    int(face_rect.top() * 4),
                    int(face_rect.right() * 4),
                    int(face_rect.bottom() * 4),
                )

                self.fr_system.process_frame(frame)

            cv2.imshow(f"Camera {self.camera_index}", frame)

            if cv2.waitKey(1) == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


def start_camera_feed(camera_index, base_folder):
    camera_feed = CameraFeed(camera_index, base_folder)
    camera_feed.start_feed()


class CameraSelector:
    def __init__(self, callback, max_cameras=10):
        self.callback = callback
        self.max_cameras = max_cameras
        self.root = tk.Tk()
        self.root.title("Select Cameras")
        self.camera_selection = None

    def get_camera_list(self):
        camera_list = []
        for i in range(self.max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(f"Camera {i}")
                cap.release()
        return camera_list

    def create_ui(self):
        label = ttk.Label(self.root, text="Select Cameras:")
        label.pack(pady=5)

        self.camera_selection = tk.Listbox(self.root, selectmode="multiple")
        for camera in self.get_camera_list():
            self.camera_selection.insert(tk.END, camera)
        self.camera_selection.pack(pady=5)

        open_button = ttk.Button(
            self.root, text="Open Selected Cameras", command=self.open_cameras
        )
        open_button.pack(pady=10)

    def open_cameras(self):
        selected_indices = [camera for camera in self.camera_selection.curselection()]
        self.root.destroy()
        self.callback(selected_indices)

    def start(self):
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":

    def start_selected_cameras(camera_indices):
        threads = []
        base_folder = os.path.abspath(r"./Faces/")
        for index in camera_indices:
            thread = threading.Thread(
                target=start_camera_feed, args=(index, base_folder)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    camera_selector = CameraSelector(start_selected_cameras)
    camera_selector.start()
