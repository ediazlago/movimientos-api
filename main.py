# main.py
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

# Base de datos
from app.database import Base, engine, verificar_conexion

# Routers
from app.routes.movimientos import router as movimientos_router
from app.routes.vista_previa import router as vista_previa_router
from app.routes.clasificacion import router as clasificacion_router
from app.routes.dashboard_datos import router as dashboard_datos_router
from app.routes.dashboard import router as dashboard_router

load_dotenv()

DEBUG = os.getenv("DEBUG") == "True"
PORT = int(os.getenv("PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
ROOT_PATH = os.getenv("ROOT_PATH", "")

app = FastAPI(title="Movimientos API", root_path=ROOT_PATH)

# Verificar conexión y crear tablas
verificar_conexion()
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(movimientos_router, prefix="/api/movimientos")
app.include_router(vista_previa_router, prefix="/vista-previa")
app.include_router(clasificacion_router)
app.include_router(dashboard_datos_router)
app.include_router(dashboard_router)

# Dashboard principal
@app.get("/", response_class=HTMLResponse)
def dashboard_principal():
    return f"""
    <html>
    <head>
        <title>Dashboard Principal</title>
    </head>
    <body>
        <h1>🏦 Dashboard Principal</h1>
        <ul>
            <li><a href="{ROOT_PATH}/clasificacion">Clasificación de gastos</a></li>
            <li><a href="{ROOT_PATH}/vista-previa">Cargar nuevo Excel</a></li>
            <li><a href="{ROOT_PATH}/dashboard-datos">Ver dashboard de datos</a></li>
        </ul>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=DEBUG)
