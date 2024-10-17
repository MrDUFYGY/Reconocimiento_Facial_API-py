from io import BytesIO
from PIL import Image
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.services import comparar_con_base
from app.models import ImagenBase, ImagenRecibida
from pydantic import BaseModel
from app.config import get_db
import base64


# Inicializamos el enrutador
router = APIRouter()

# Ruta para agregar una nueva imagen base
@router.post("/imagen_base/")
def agregar_imagen_base(ubicacion: str, db: Session = Depends(get_db)):
    nueva_imagen_base = ImagenBase(Ubicacion=ubicacion)
    db.add(nueva_imagen_base)
    db.commit()
    db.refresh(nueva_imagen_base)
    return {"mensaje": "Imagen base agregada correctamente", "id": nueva_imagen_base.Id}

# Ruta para agregar una nueva imagen recibida
@router.post("/imagen_recibida/")
def agregar_imagen_recibida(ubicacion: str, db: Session = Depends(get_db)):
    nueva_imagen_recibida = ImagenRecibida(Ubicacion=ubicacion)
    db.add(nueva_imagen_recibida)
    db.commit()
    db.refresh(nueva_imagen_recibida)
    return {"mensaje": "Imagen recibida agregada correctamente", "id": nueva_imagen_recibida.Id}

# Modelo para recibir la solicitud
class ImageRequest(BaseModel):
    image: str  # Se recibe la imagen en formato Base64

# Ruta POST para recibir imagen, convertir a JPG y comparar
@router.post("/comparar_imagen")
async def comparar_imagen_route(request: ImageRequest, db: Session = Depends(get_db)):
    try:
        # Convertir la imagen Base64 a bytes
        image_bytes = BytesIO(base64.b64decode(request.image))

        # Convertir los bytes a una imagen JPG
        image = Image.open(image_bytes)
        image = image.convert("RGB")  # Convertir a formato RGB para JPG
        image_path = "temp_image.jpg"  # Guardar la imagen temporalmente

        # Guardar como JPG temporal
        image.save(image_path, "JPEG")

        # Llamar a la función para comparar la imagen con la base de imágenes
        resultado = await comparar_con_base(image_path, db)

        return {"resultado": resultado}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)