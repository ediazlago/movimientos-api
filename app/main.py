# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

# Configuración básica
DEBUG = os.getenv("DEBUG") == "True"
PORT = int(os.getenv("PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Inicializar la app
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar y registrar rutas
from app.routes.movimientos import router as movimientos_router
app.include_router(movimientos_router, prefix="/api/movimientos")

# Ruta raíz
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a movimientos_api"}

# Ejecutar la app (solo si se corre directamente)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=DEBUG)