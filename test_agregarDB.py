import os
from app.config import SessionLocal
from app.models import ImagenBase, ImagenRecibida


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def agregar_imagen_base(db, ruta_imagen, descripcion=None):
    # Obtener el nombre y formato desde la ruta
    nombre, formato = obtener_nombre_y_formato(ruta_imagen)

    # Leer la imagen en formato binario
    datos_imagen = leer_imagen_en_binario(ruta_imagen)

    if datos_imagen is None:
        print("Error: No se pudo leer la imagen.")
        return

    # Descripción por defecto si no se proporciona
    if not descripcion:
        descripcion = "Imagen base sin descripción."

    nueva_imagen_base = ImagenBase(
        Nombre=nombre,
        Formato=formato,
        DatosImagen=datos_imagen,
        RutaImagen=ruta_imagen,
        Descripcion=descripcion
    )
    db.add(nueva_imagen_base)
    db.commit()
    db.refresh(nueva_imagen_base)
    return nueva_imagen_base


def agregar_imagen_recibida(db, ruta_imagen, ubicacion=None, descripcion=None):
    # Obtener el nombre y formato desde la ruta
    nombre, formato = obtener_nombre_y_formato(ruta_imagen)

    # Leer la imagen en formato binario
    datos_imagen = leer_imagen_en_binario(ruta_imagen)

    if datos_imagen is None:
        print("Error: No se pudo leer la imagen.")
        return

    # Ubicación y descripción por defecto si no se proporcionan
    if not ubicacion:
        ubicacion = "Ubicación no especificada."
    if not descripcion:
        descripcion = "Imagen recibida sin descripción."

    nueva_imagen_recibida = ImagenRecibida(
        Nombre=nombre,
        Formato=formato,
        DatosImagen=datos_imagen,
        RutaImagen=ruta_imagen,
        Ubicacion=ubicacion,
        Descripcion=descripcion
    )
    db.add(nueva_imagen_recibida)
    db.commit()
    db.refresh(nueva_imagen_recibida)
    return nueva_imagen_recibida


# Función para leer una imagen desde una ruta y convertirla a formato binario
def leer_imagen_en_binario(ruta_imagen):
    try:
        with open(ruta_imagen, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_imagen}")
        return None


# Función para obtener el nombre y formato del archivo
def obtener_nombre_y_formato(ruta_imagen):
    nombre_completo = os.path.basename(ruta_imagen)  # Obtener el nombre del archivo con la extensión
    nombre, formato = os.path.splitext(nombre_completo)  # Dividir el nombre y la extensión
    return nombre, formato.lstrip('.')  # Quitar el punto de la extensión


def main():
    # Crear una sesión de base de datos
    db = SessionLocal()

    try:
        # Subir una imagen base desde una ruta estática
        ruta_base = "C:/Users/fjuarez/Desktop/a/ryan2.jpg"

        # Agregar la imagen base utilizando solo la ruta
        imagen_base = agregar_imagen_base(
            db=db,
            ruta_imagen=ruta_base,
            descripcion="Imagen base agregada automáticamente."
        )
        print(f"Imagen base agregada: {imagen_base.IdImagenBase}")

        # Subir una imagen recibida desde una ruta estática
        ruta_recibida = "C:/Users/fjuarez/Desktop/a/ryan3.jpg"

        # Agregar la imagen recibida utilizando solo la ruta
        imagen_recibida = agregar_imagen_recibida(
            db=db,
            ruta_imagen=ruta_recibida,
            ubicacion="Ubicación de prueba",
            descripcion="Imagen recibida agregada automáticamente."
        )
        print(f"Imagen recibida agregada: {imagen_recibida.IdImagenRecibida}")

    finally:
        # Cerrar la sesión de base de datos
        db.close()


if __name__ == "__main__":
    main()
