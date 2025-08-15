# app/models/movimiento.py

from pydantic import BaseModel
from datetime import datetime

class Movimiento(BaseModel):
    id: int
    tipo: str
    cantidad: float
    fecha: datetime
