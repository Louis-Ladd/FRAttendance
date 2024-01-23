import cv2
import face_recognition
import threading
import os
import pickle

FACES_FOLDER = r'C:\Users\dhirao\Pictures\Faces_2.0'
FACES_FILE = os.path.join(FACES_FOLDER, 'known_faces.pkl')

# Initialize face recognition
known_faces = {}
next_face_id = 1

def load_known_faces():
    global known_faces, next_face_id
    if os.path.exists(FACES_FILE):
        with open(FACES_FILE, 'rb') as file:
            known_faces, next_face_id = pickle.load(file)

def save_known_faces():
    if not os.path.exists(FACES_FOLDER):
        os.makedirs(FACES_FOLDER)
    with open(FACES_FILE, 'wb') as file:
        pickle.dump((known_faces, next_face_id), file)

def add_face(face_encoding):
    global next_face_id
    face_name = f"face{next_face_id}"
    known_faces[face_name] = face_encoding
    print(f"{face_name} added")
    next_face_id += 1
    save_known_faces()

def recognize_face(face_encoding):
    for name, known_encoding in known_faces.items():
        result = face_recognition.compare_faces([known_encoding], face_encoding)
        if result[0]:
            return name
    return "Unknown"

# Face detection function
def detect_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = recognize_face(face_encoding)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        if name == "Unknown":
            add_face(face_encoding)

# Camera capture thread
def camera_thread(camera_index):
    video_capture = cv2.VideoCapture(camera_index)

    while True:
        ret, frame = video_capture.read()
        detect_face(frame)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Main program
if __name__ == "__main__":
    # Load known faces from file
    load_known_faces()

    # Choose the camera index (e.g., 0 for default camera, 1 for an additional camera)
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
