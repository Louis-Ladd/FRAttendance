import cv2
import os
import tkinter as tk
from tkinter import ttk
import threading
import time


class CameraFeed:
    def __init__(self, camera_index, pictures_folder):
        self.camera_index = int(camera_index)
        self.pictures_folder = pictures_folder
        self.cap = cv2.VideoCapture(self.camera_index)

    def start_feed(self):
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}.")
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print(f"Error: Could not read frame from camera {self.camera_index}.")
                break

            cv2.imshow(f"Camera {self.camera_index}", frame)

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
        pictures_folder = os.path.abspath(
            r"./Faces/"
        )  # Define the pictures folder path

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
