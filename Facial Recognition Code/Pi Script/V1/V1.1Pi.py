import cv2
import dlib
import os
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

    def send_image_to_server(self, image_path):
        """
        Function to send an image to the server.
        (Currently not in use until the backend server is set up)
        """
        url = "http://[Django-Server-IP]:[Port]/upload/"  # Replace with your Django server's IP and port
        files = {"image": open(image_path, "rb")}
        response = requests.post(url, files=files)
        print(response.text)

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
                face_filename = os.path.join(self.save_dir, f"face_{self.face_id}.jpg")
                cv2.imwrite(face_filename, face_img)
                # self.send_image_to_server(face_filename)  # Uncomment when server is ready
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
