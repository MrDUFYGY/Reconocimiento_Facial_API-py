from app.config import SessionLocal
from app.models import ImagenBase, ImagenRecibida

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para consultar todas las imágenes base
def consultar_imagenes_base(db):
    # Consultar todas las imágenes base en la base de datos
    imagenes_base = db.query(ImagenBase).all()

    # Imprimir los resultados
    print("\nImágenes Base:")
    for imagen in imagenes_base:
        print(f"ID: {imagen.IdImagenBase}, Nombre: {imagen.Nombre}, Formato: {imagen.Formato}, "
              f"Ruta: {imagen.RutaImagen}, Descripción: {imagen.Descripcion}, Fecha Subida: {imagen.FechaSubida}")

# Función para consultar todas las imágenes recibidas
def consultar_imagenes_recibidas(db):
    # Consultar todas las imágenes recibidas en la base de datos
    imagenes_recibidas = db.query(ImagenRecibida).all()

    # Imprimir los resultados
    print("\nImágenes Recibidas:")
    for imagen in imagenes_recibidas:
        print(f"ID: {imagen.IdImagenRecibida}, Nombre: {imagen.Nombre}, Formato: {imagen.Formato}, "
              f"Ruta: {imagen.RutaImagen}, Ubicación: {imagen.Ubicacion}, Descripción: {imagen.Descripcion}, "
              f"Fecha Subida: {imagen.FechaSubida}")

def main():
    # Crear una sesión de base de datos
    db = SessionLocal()

    try:
        # Consultar todas las imágenes base
        consultar_imagenes_base(db)

        # Consultar todas las imágenes recibidas
        consultar_imagenes_recibidas(db)

    finally:
        # Cerrar la sesión de base de datos
        db.close()

if __name__ == "__main__":
    main()
