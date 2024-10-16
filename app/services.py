import face_recognition
import os
from fastapi.responses import JSONResponse
from app.config import SessionLocal
from app.models import ComparacionResultado
from sqlalchemy.orm import Session


# Carpeta donde se guardarán las imágenes temporalmente
BASE_IMAGE_DIR = "images/base"

# Función para comparar la imagen recibida con el banco de imágenes en la carpeta base
async def comparar_con_base_b(imagen_recibida):

    # Verificar que la carpeta base exista
    if not os.path.exists(BASE_IMAGE_DIR):
        return JSONResponse(content={"error": "No se encontró la carpeta base de imágenes."}, status_code=400)

    # Guardar temporalmente la imagen recibida
    received_image_path = f"images/recibida/{imagen_recibida.filename}"
    with open(received_image_path, "wb") as f:
        f.write(await imagen_recibida.read())

    # Cargar la imagen recibida
    received_image = face_recognition.load_image_file(received_image_path)

    try:
        # Obtener el encoding de la imagen recibida
        received_encoding = face_recognition.face_encodings(received_image)[0]
    except IndexError:
        return JSONResponse(content={"error": "No se detectó ningún rostro en la imagen recibida."}, status_code=400)

    # Recorrer todas las imágenes de la carpeta base
    for base_image_filename in os.listdir(BASE_IMAGE_DIR):
        base_image_path = os.path.join(BASE_IMAGE_DIR, base_image_filename)

        # Cargar la imagen base y obtener su encoding
        base_image = face_recognition.load_image_file(base_image_path)
        try:
            base_encoding = face_recognition.face_encodings(base_image)[0]
        except IndexError:
            continue  # Si no se encuentra un rostro en una imagen base, pasar a la siguiente

        # Comparar la imagen recibida con la imagen base
        resultado = face_recognition.compare_faces([base_encoding], received_encoding)

        if resultado[0]:
            return {"resultado": f"La imagen coincide con {base_image_filename}"}

    # Si no hay coincidencias
    return {"resultado": "No hay coincidencias con las imágenes de la base"}


# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para almacenar el resultado de la comparación en la base de datos
def guardar_resultado(db: Session, imagen_recibida: str, imagen_base: str, resultado: str):
    resultado_comparacion = ComparacionResultado(
        imagen_recibida=imagen_recibida, imagen_base=imagen_base, resultado=resultado
    )
    db.add(resultado_comparacion)
    db.commit()
    db.refresh(resultado_comparacion)
    return resultado_comparacion


async def comparar_con_base(imagen_recibida, db: Session):
    # Guardar la imagen recibida temporalmente
    received_image_path = f"images/recibida/{imagen_recibida.filename}"
    with open(received_image_path, "wb") as f:
        f.write(await imagen_recibida.read())

    # Cargar la imagen recibida
    received_image = face_recognition.load_image_file(received_image_path)
    try:
        received_encoding = face_recognition.face_encodings(received_image)[0]
    except IndexError:
        return JSONResponse(content={"error": "No se detectó ningún rostro en la imagen recibida."}, status_code=400)

    # Iterar sobre todas las imágenes base
    for base_image_filename in os.listdir(BASE_IMAGE_DIR):
        base_image_path = os.path.join(BASE_IMAGE_DIR, base_image_filename)
        base_image = face_recognition.load_image_file(base_image_path)
        try:
            base_encoding = face_recognition.face_encodings(base_image)[0]
        except IndexError:
            continue  # Pasar a la siguiente si no se detecta rostro

        # Comparar las imágenes
        resultado = face_recognition.compare_faces([base_encoding], received_encoding)

        if resultado[0]:
            guardar_resultado(db, imagen_recibida.filename, base_image_filename, "Coincide")
            return {"resultado": f"La imagen coincide con {base_image_filename}"}

    guardar_resultado(db, imagen_recibida.filename, "Ninguna", "No coincide")
    return {"resultado": "No hay coincidencias con las imágenes de la base"}