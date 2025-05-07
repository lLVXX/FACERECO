import cv2
import face_recognition
from core.models import Estudiante
from django.core.files.storage import default_storage

# Listas globales
known_encodings = []
known_names = []

def load_known_faces_from_db():
    """
    Carga los rostros conocidos desde la base de datos Estudiante,
    codifica sus fotos y guarda sus nombres y codificaciones.
    """
    global known_encodings, known_names
    known_encodings.clear()
    known_names.clear()

    estudiantes = Estudiante.objects.all()

    for estudiante in estudiantes:
        if estudiante.photo:
            try:
                with default_storage.open(estudiante.photo.name, 'rb') as image_file:
                    image = face_recognition.load_image_file(image_file)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        known_encodings.append(encodings[0])
                        full_name = f"{estudiante.nombre} {estudiante.apellido}"
                        known_names.append(full_name)
            except Exception as e:
                print(f"Error procesando imagen de {estudiante}: {e}")

def generate_video_stream():
    """
    Inicia la cámara y compara los rostros detectados con los conocidos.
    Dibuja un rectángulo y el nombre si se encuentra una coincidencia.
    """
    load_known_faces_from_db()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise Exception("No se pudo acceder a la cámara.")

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Reducción de tamaño para mejorar velocidad
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

            # Redimensionar las coordenadas al tamaño original
            top, right, bottom, left = [val * 4 for val in location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()
