from sqlalchemy.orm import Session
from app.models.movimiento import Movimiento

def listar_movimientos(db: Session):
    return db.query(Movimiento).all()

def crear_movimiento(db: Session, movimiento_data):
    nuevo = Movimiento(**movimiento_data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

