from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.movimiento import Movimiento as MovimientoModel
from app.controllers.movimiento_controller import listar_movimientos, crear_movimiento
from app.schemas.movimiento import MovimientoCreate, MovimientoRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[MovimientoRead])
def obtener_movimientos(db: Session = Depends(get_db)):
    return listar_movimientos(db)

@router.post("/", response_model=MovimientoRead)
def nuevo_movimiento(movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    return crear_movimiento(db, movimiento)
