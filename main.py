from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, verificar_conexion
from app.routes.movimientos import router as movimientos_router
from app.routes.vista_previa import router as vista_previa_router
import os

load_dotenv()

DEBUG = os.getenv("DEBUG") == "True"
PORT = int(os.getenv("PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

app = FastAPI()

verificar_conexion()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movimientos_router, prefix="/api/movimientos")
app.include_router(vista_previa_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=DEBUG)