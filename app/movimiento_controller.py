# app/controllers/movimiento_controller.py

from app.models.movimiento import Movimiento
from datetime import datetime

# Simulación de base de datos en memoria
db = []

def listar_movimientos():
    return db

def crear_movimiento(data: Movimiento):
    db.append(data)
    return data
