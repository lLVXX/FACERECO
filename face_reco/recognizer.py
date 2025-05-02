import cv2
import face_recognition
from core.models import Student
from django.core.files.storage import default_storage

known_encodings = []
known_names = []

def load_known_faces_from_db():
    global known_encodings, known_names
    known_encodings.clear()
    known_names.clear()

    students = Student.objects.all()

    for student in students:
        if student.photo:
            with default_storage.open(student.photo.name, 'rb') as image_file:
                image = face_recognition.load_image_file(image_file)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    full_name = f"{student.first_name} {student.name}"
                    known_names.append(full_name)

def generate_video_stream():
    load_known_faces_from_db()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise Exception("Camera not accessible")

    while True:
        success, frame = camera.read()
        if not success:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Desconocido"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

            top, right, bottom, left = [val * 4 for val in location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()
