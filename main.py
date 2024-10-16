from fastapi import FastAPI
from app.routes import router

# Inicializamos la aplicación FastAPI
app = FastAPI()

# Incluimos las rutas definidas en routes.py
app.include_router(router)

# Verificar el estado del servidor
@app.get("/status")
def get_status():
    return {"status": "API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
