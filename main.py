from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

# Inicializamos la aplicación FastAPI
app = FastAPI()

# Configuración de CORS para permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

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
