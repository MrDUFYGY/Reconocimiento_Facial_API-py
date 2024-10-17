import os
import face_recognition
import io
from sqlalchemy.orm import Session
from app.models import ComparacionResultado, ImagenRecibida
from datetime import datetime
import pyodbc
from PIL import Image

# Directorio temporal opcional
TEMP_IMAGE_DIR = "images/temp_img"
if not os.path.exists(TEMP_IMAGE_DIR):
    os.makedirs(TEMP_IMAGE_DIR)

# Conexión a la base de datos para ejecutar el stored procedure
def obtener_imagenes_base():
    # Datos de conexión
    server = 'FJUAREZ\\SQLEXPRESS'
    database = 'ReconocimientoFacial'
    username = 'sa'
    password = 'Inquieto.17'

    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    cursor.execute("EXEC GetAllImagenBase")
    rows = cursor.fetchall()

    imagenes_base = []

    for row in rows:
        # Obtener los datos binarios de la imagen desde la base de datos
        imagen_binaria = row.DatosImagen
        if imagen_binaria is not None:
            # Agregar la imagen a la lista para la comparación
            imagenes_base.append((row.IdImagenBase, imagen_binaria))

    cursor.close()
    conn.close()

    return imagenes_base

# Función para convertir datos binarios en formato que face_recognition pueda procesar
def cargar_imagen_desde_binarios(imagen_binaria):
    try:
        image = Image.open(io.BytesIO(imagen_binaria))
        image_array = face_recognition.load_image_file(io.BytesIO(imagen_binaria))
        return image_array
    except Exception as e:
        print(f"Error al cargar la imagen desde binario: {e}")
        return None

# Función para comparar la imagen recibida con el banco de imágenes obtenidas del stored procedure
def comparar_con_base(image_data: bytes, db: Session):
    # Registrar la imagen recibida en la base de datos
    nueva_imagen_recibida = ImagenRecibida(
        Nombre="imagen_recibida.jpg",
        Formato="JPEG",
        FechaSubida=datetime.now(),
        DatosImagen=image_data,
        RutaImagen="Ruta no especificada",
        Ubicacion="Ubicación de la imagen recibida"
    )
    db.add(nueva_imagen_recibida)
    db.commit()
    db.refresh(nueva_imagen_recibida)
    imagen_recibida_id = nueva_imagen_recibida.IdImagenRecibida

    # Cargar la imagen recibida
    received_image = face_recognition.load_image_file(io.BytesIO(image_data))

    try:
        # Obtener el encoding de la imagen recibida
        received_encoding = face_recognition.face_encodings(received_image)[0]
    except IndexError:
        return {"resultado": "No se detectó ningún rostro en la imagen recibida."}

    # Recuperar las imágenes base desde el stored procedure
    imagenes_base = obtener_imagenes_base()

    # Variable para controlar si hubo coincidencia
    hay_coincidencia = False

    # Iterar sobre las imágenes base obtenidas
    for imagen_base_id, imagen_binaria in imagenes_base:
        # Cargar la imagen base desde los datos binarios
        base_image = cargar_imagen_desde_binarios(imagen_binaria)
        if base_image is None:
            continue

        try:
            # Obtener el encoding de la imagen base
            base_encoding = face_recognition.face_encodings(base_image)[0]
        except IndexError:
            continue  # Si no hay rostros, saltar la imagen

        # Comparar la imagen recibida con la imagen base
        resultado = face_recognition.compare_faces([base_encoding], received_encoding)
        distancia = face_recognition.face_distance([base_encoding], received_encoding)
        similitud = (1 - distancia[0]) * 100  # Convertir distancia a porcentaje de similitud

        if resultado[0]:
            hay_coincidencia = True
            # Guardar el resultado en la base de datos
            guardar_resultado(db, imagen_recibida_id, similitud, "Coincide", imagen_base_id)
            return f"La imagen coincide con la imagen de IdImagenBase: {imagen_base_id}"

    # Si no hubo coincidencias, asignar IdImagenBase = 20 en ComparacionResultado
    if not hay_coincidencia:
        guardar_resultado(db, imagen_recibida_id, 0.0, "No coincide", 20)
        return "No hay coincidencias con las imágenes de la base"

# Función para guardar el resultado en la base de datos
def guardar_resultado(db: Session, imagen_recibida_id: int, resultado_comparacion: float, ubicacion: str, imagen_base_id: int):
    comparacion = ComparacionResultado(
        IdImagenRecibida=imagen_recibida_id,
        IdImagenBase=imagen_base_id,
        ResultadoComparacion=resultado_comparacion,
        Ubicacion=ubicacion
    )
    db.add(comparacion)
    db.commit()
    db.refresh(comparacion)
    return comparacion
