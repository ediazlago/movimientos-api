from app.models.movimiento import Movimiento

db = []

def listar_movimientos():
    return db

def crear_movimiento(data: Movimiento):
    db.append(data)
    return data
