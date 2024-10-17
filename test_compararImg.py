import pyodbc
from PIL import Image
import io
import face_recognition
import os

# Datos de conexión
server = 'FJUAREZ\\SQLEXPRESS'
database = 'ReconocimientoFacial'
username = 'sa'
password = 'Inquieto.17'

# Directorio temporal para guardar las imágenes (asegúrate de que existe)
temp_dir = r'C:\Users\fjuarez\Desktop\temp_imagenes'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Conectar a SQL Server
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Crear un cursor
cursor = conn.cursor()

# Ejecutar el stored procedure para obtener las imágenes
cursor.execute("EXEC GetAllImagenBase")

# Obtener los resultados
rows = cursor.fetchall()

# Lista para almacenar las imágenes
images_db = []

# Convertir las imágenes a archivos temporales y almacenarlas
for idx, row in enumerate(rows):
    binary_image = row.DatosImagen  # Cambiado a DatosImagen
    if binary_image is not None:
        try:
            # Guardar la imagen temporalmente
            image_path = os.path.join(temp_dir, f"image_{idx}.jpg")
            with open(image_path, "wb") as f:
                f.write(binary_image)

            # Cargar la imagen temporalmente para face_recognition
            images_db.append(image_path)
        except Exception as e:
            print(f"Error al procesar la imagen {idx}: {e}")

# Cerrar la conexión
cursor.close()
conn.close()

# Cargar la imagen recibida "ryan3"
image_received = face_recognition.load_image_file(r"C:\Users\fjuarez\Desktop\a\ryan3.jpg")

# Obtener las codificaciones faciales de la imagen recibida
encoding_received = face_recognition.face_encodings(image_received)[0]

# Iterar sobre las imágenes obtenidas de la base de datos
for image_path in images_db:
    try:
        # Cargar la imagen temporalmente desde el archivo guardado
        image_array = face_recognition.load_image_file(image_path)

        # Obtener las codificaciones faciales de la imagen de la base de datos
        encoding_db = face_recognition.face_encodings(image_array)

        # Comprobar si la imagen contiene una cara antes de intentar la comparación
        if len(encoding_db) > 0:
            encoding_db = encoding_db[0]

            # Comparar las codificaciones faciales
            results = face_recognition.compare_faces([encoding_db], encoding_received)

            if results[0]:
                print(f"¡Coincidencia encontrada con una imagen de la base de datos! Imagen: {image_path}")
            else:
                print(f"No hay coincidencia. Imagen: {image_path}")
        else:
            print(f"No se encontró ninguna cara en la imagen de la base de datos. Imagen: {image_path}")
    except Exception as e:
        print(f"Error al procesar la imagen para comparación: {e}")
