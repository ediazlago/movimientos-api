# app/routes/movimientos.py

from fastapi import APIRouter
from app.models.movimiento import Movimiento
from app.controllers.movimiento_controller import listar_movimientos, crear_movimiento

router = APIRouter()

@router.get("/")
def obtener_movimientos():
    return listar_movimientos()

@router.post("/")
def nuevo_movimiento(movimiento: Movimiento):
    return crear_movimiento(movimiento)
