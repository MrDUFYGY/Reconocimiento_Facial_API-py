from fastapi import FastAPI, Response
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

# Inicializamos la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # Agrega más orígenes si es necesario
    "http://127.0.0.1:3000"
]

# Añadimos el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Ruta para manejar solicitudes OPTIONS
@app.options("/comparar_imagen", response_class=Response)
def preflight_handler():
    return Response(headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })

# Incluimos las rutas definidas en routes.py
app.include_router(router)

# Verificar el estado del servidor
@app.get("/status")
def get_status():
    return {"status": "API funcionando correctamente"}

# Iniciar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
