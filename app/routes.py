from fastapi import APIRouter, File, UploadFile
from app.services import comparar_con_base
from fastapi.responses import JSONResponse

# Inicializamos el enrutador
router = APIRouter()

# Ruta POST para comparar una imagen con el banco de imágenes en la carpeta base
@router.post("/comparar_imagen")
async def comparar_imagen_route(imagen_recibida: UploadFile = File(...)):
    try:
        # Llamamos al servicio que se encarga de la comparación
        resultado = await comparar_con_base(imagen_recibida)
        return resultado
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
