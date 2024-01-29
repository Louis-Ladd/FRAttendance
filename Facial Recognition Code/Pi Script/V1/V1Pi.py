import cv2
import dlib
import os

# Initialize the dlib face detector
detector = dlib.get_frontal_face_detector()

# Camera index
camera_index = 1

# Open the camera
cap = cv2.VideoCapture(camera_index)

# Directory to save face images
save_dir = "captured_faces"
os.makedirs(save_dir, exist_ok=True)

face_id = 0
tracked_faces = []

# Distance threshold for considering a face as new
distance_threshold = 50

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)

    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        # Check if this face is new or already tracked
        new_face = True
        for tracked_face in tracked_faces:
            tx, ty, tw, th = tracked_face
            distance = ((tx - x) ** 2 + (ty - y) ** 2) ** 0.5
            if distance < distance_threshold:
                new_face = False
                break

        if new_face:
            tracked_faces.append((x, y, w, h))
            face_img = frame[y : y + h, x : x + w]
            face_filename = os.path.join(save_dir, f"face_{face_id}.jpg")
            cv2.imwrite(face_filename, face_img)
            face_id += 1

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
