from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, movimientos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movimientos.router)

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a la API de movimientos!"}