import sys
import os
import cv2
import face_recognition
import numpy as np
import pickle
import pyodbc
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer


def connect_db():
    return pyodbc.connect(
        'DRIVER={SQL Server};SERVER=MESCHZHE01;DATABASE=ofbiz;UID=pbilogin;PWD=kmcj123456')


def mark_attendance(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO UST_ATTENDANCE (EMP_NAME, LOG_TIME) VALUES (?, CURRENT_TIMESTAMP)", name)
    conn.commit()
    conn.close()
    print(f"Attendance marked for {name}")


def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    for file in os.listdir():
        if file.endswith("_encoding.pkl"):
            name = file.split("_")[0]
            with open(file, 'rb') as f:
                known_face_encodings.append(pickle.load(f))
                known_face_names.append(name)
    return known_face_encodings, known_face_names


class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.known_face_encodings, self.known_face_names = load_known_faces()
        self.cam = None

    def init_ui(self):
        self.setWindowTitle('Face Recognition Attendance System')

        self.name_label = QLabel('Name:')
        self.name_input = QLineEdit(self)

        self.register_button = QPushButton('Register Face', self)
        self.register_button.clicked.connect(self.register_face)

        self.capture_button = QPushButton('Capture & Recognize', self)
        self.capture_button.clicked.connect(self.capture_and_recognize)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.capture_button)

        self.setLayout(layout)

    def register_face(self):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a name.")
            return

        self.cam = cv2.VideoCapture(0)
        face_encodings = []

        QMessageBox.information(self, "Instructions", "Press 'c' to capture a picture, 'q' to quit and save the encodings.")

        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("Failed to capture image. Check your camera.")
                break

            cv2.imshow("Capture Face", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                face_locations = face_recognition.face_locations(frame)
                current_encodings = face_recognition.face_encodings(frame, face_locations)
                if current_encodings:
                    face_encodings.append(current_encodings[0])
                    print(f"Captured image {len(face_encodings)}")
            elif key == ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()

        if face_encodings:
            averaged_encoding = np.mean(face_encodings, axis=0)
            with open(f"{name}_encoding.pkl", 'wb') as f:
                pickle.dump(averaged_encoding, f)
            print(f"{name}'s face registered with {len(face_encodings)} images.")
            QMessageBox.information(self, "Success", f"{name}'s face registered successfully.")
            self.known_face_encodings, self.known_face_names = load_known_faces()
        else:
            QMessageBox.warning(self, "Registration Failed", "No face detected. Try again.")

    def capture_and_recognize(self):
        self.cam = cv2.VideoCapture(0)

        while True:
            ret, frame = self.cam.read()
            if not ret:
                break

            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    similarity = 1 - face_distances[best_match_index]
                    name = self.known_face_names[best_match_index]
                    if similarity > 0.8:
                        print(similarity)
                        mark_attendance(name)
                        QMessageBox.information(self, "Attendance", f"Attendance marked for {name}")
                        self.cam.release()
                        return
                    else:
                        print(f"Similarity for {name} is too low: {similarity}")
                else:
                    print("No match found.")

            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    face_recognition_app = FaceRecognitionApp()
    face_recognition_app.show()
    sys.exit(app.exec())
