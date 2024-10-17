import face_recognition
import os
from sqlalchemy.orm import Session
from app.models import ComparacionResultado, ImagenBase


# Carpeta donde se guardarán las imágenes base y recibidas
BASE_IMAGE_DIR = "images/base"
RECEIVED_IMAGE_DIR = "images/recibida"

# Función para comparar la imagen recibida con el banco de imágenes en la carpeta base
async def comparar_con_base(image_path: str, db: Session):
    # Cargar la imagen recibida
    received_image = face_recognition.load_image_file(image_path)

    try:
        # Obtener el encoding de la imagen recibida
        received_encoding = face_recognition.face_encodings(received_image)[0]
    except IndexError:
        return {"resultado": "No se detectó ningún rostro en la imagen recibida."}

    # Recorrer todas las imágenes base
    for base_image_filename in os.listdir(BASE_IMAGE_DIR):
        base_image_path = os.path.join(BASE_IMAGE_DIR, base_image_filename)

        # Cargar la imagen base y obtener su encoding
        base_image = face_recognition.load_image_file(base_image_path)
        try:
            base_encoding = face_recognition.face_encodings(base_image)[0]
        except IndexError:
            continue  # Si no hay rostros, saltar la imagen

        # Comparar la imagen recibida con la imagen base
        resultado = face_recognition.compare_faces([base_encoding], received_encoding)

        if resultado[0]:
            # Si hay coincidencia, guardar en la base de datos
            imagen_base = db.query(ImagenBase).filter(ImagenBase.Nombre == base_image_filename).first()
            guardar_resultado(db, None, imagen_base.IdImagenBase, "Coincide")
            return f"La imagen coincide con {base_image_filename}"

    # Si no hay coincidencias
    guardar_resultado(db, None, None, "No coincide")
    return "No hay coincidencias con las imágenes de la base"

# Función para guardar el resultado en la base de datos
def guardar_resultado(db: Session, imagen_recibida_id: int, imagen_base_id: int, resultado: str):
    comparacion = ComparacionResultado(
        IdImagenRecibida=imagen_recibida_id,
        IdImagenBase=imagen_base_id,
        ResultadoComparacion=100.0 if resultado == "Coincide" else 0.0,
        Ubicacion="Coincidencia" if resultado == "Coincide" else "No coincidencia"
    )
    db.add(comparacion)
    db.commit()
    db.refresh(comparacion)
    return comparacion