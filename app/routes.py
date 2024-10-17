from io import BytesIO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.services import comparar_con_base
from app.config import get_db
from pydantic import BaseModel
import base64
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializamos el enrutador
router = APIRouter()

# Modelo para recibir la solicitud
class ImageRequest(BaseModel):
    image: str  # Se recibe la imagen en formato Base64

# Ruta POST para recibir imagen y comparar
@router.post("/comparar_imagen")
def comparar_imagen_route(request: ImageRequest, db: Session = Depends(get_db)):
    try:
        # Obtener el string Base64 de la imagen
        image_base64 = request.image

        # Eliminar el prefijo si está presente (ejemplo: "data:image/jpeg;base64,")
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        # Convertir la imagen Base64 a bytes
        image_data = base64.b64decode(image_base64)

        # Llamar a la función para comparar la imagen con la base de imágenes
        resultado = comparar_con_base(image_data, db)

        return {"resultado": resultado}
    except Exception as e:
        logger.error(f"Error en /comparar_imagen: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
