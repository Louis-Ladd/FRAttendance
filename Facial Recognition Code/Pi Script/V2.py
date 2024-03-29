import cv2
import dlib
import os
import socket
from threading import Thread
import requests


class FaceDetector:
    def __init__(self, camera_index=0, save_dir="captured_faces"):
        self.detector = dlib.get_frontal_face_detector()
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.face_id = 0
        self.tracked_faces = []
        self.distance_threshold = 50

    def send_image_to_server(self, image_path, ip : str):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.settimeout(0.2)
            client.connect((ip, 1002))
        except TimeoutError:
            print("TimeoutError: is the server listening? is the PORT correct? is the IP correct?")
            client.close()
            return
        except ConnectionRefusedError:
            print("ConnectionRefusedError: is the server listening? is the PORT correct? is the IP correct?")
            client.close()
            return

        try:
            with open(image_path, "rb") as file:
                image_data = file.read(2048)

                while image_data:
                    client.send(image_data)
                    image_data = file.read(2048)
        except:
            print("Unknown file error: unable to finish transfer with server")
            client.close()
            return

        print(f"successful: successfully sent face to server at {ip}")
        client.close()

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            new_face = True

            for tracked_face in self.tracked_faces:
                tx, ty, tw, th = tracked_face
                distance = ((tx - x) ** 2 + (ty - y) ** 2) ** 0.5
                if distance < self.distance_threshold:
                    new_face = False
                    break

            if new_face:
                self.tracked_faces.append((x, y, w, h))
                face_img = frame[y : y + h, x : x + w]
                face_filename = os.path.join(self.save_dir, f"face_{self.face_id}.png")
                try:
                    cv2.imwrite(face_filename, face_img)
                except cv2.error as e:
                    print(f"Open CV Error: {e.msg}")
                print("Captured face: attempting to send to server...")
                print(f"Saving at {face_filename}")
                #self.send_image_to_server(face_filename)
                t = Thread(target=self.send_image_to_server, args=[face_filename, "192.168.5.7"])
                t.run()
                self.face_id += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        return True

    def run(self):
        while True:
            if not self.process_frame():
                break
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_detector = FaceDetector()
    face_detector.run()
