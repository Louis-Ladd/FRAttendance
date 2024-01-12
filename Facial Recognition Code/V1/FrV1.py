import cv2
import face_recognition
import os
import numpy as np


def load_known_faces(pictures_folder):
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


def assess_image_quality(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def is_new_face(face_encoding, known_encodings, tolerance=0.6):
    if not known_encodings:
        return True
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    return np.all(distances >= tolerance)


def capture_images_with_face_detection():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    known_faces_folder = r"C:\Users\tyler\OneDrive\Pictures\Faces"
    known_faces = load_known_faces(known_faces_folder)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture frame.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(
                known_faces["encodings"], face_encoding, tolerance=0.6
            )
            face_label = "Unknown"

            top, right, bottom, left = [v * 4 for v in face_location]
            face_image = frame[top:bottom, left:right]
            image_quality = assess_image_quality(face_image)

            if any(matches):
                first_match_index = matches.index(True)
                face_label = known_faces["names"][first_match_index]

                old_image_path = os.path.join(known_faces_folder, f"{face_label}.jpg")
                if os.path.exists(old_image_path):
                    old_image = cv2.imread(old_image_path)
                    old_image_quality = assess_image_quality(old_image)

                    if image_quality > old_image_quality:
                        cv2.imwrite(old_image_path, face_image)
                        print(
                            f"Updated image for {face_label} with a better quality image."
                        )
            elif is_new_face(face_encoding, known_faces["encodings"]):
                face_label = f"face_{len(known_faces['encodings']) + 1}"
                known_faces["encodings"].append(face_encoding)
                known_faces["names"].append(face_label)
                cv2.imwrite(
                    os.path.join(known_faces_folder, f"{face_label}.jpg"), face_image
                )
                print(f"New face detected and saved as {face_label}")

            # Draw a box around the face and label it
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

        # Display the resulting image
        cv2.imshow("Video Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_images_with_face_detection()
