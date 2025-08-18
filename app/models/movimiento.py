# app/models/movimiento.py
from pydantic import BaseModel, validator
from datetime import datetime

class Movimiento(BaseModel):
    fecha_operacion: datetime
    concepto: str
    fecha_valor: datetime
    importe: float
    saldo: float

    @validator("concepto")
    def concepto_no_vacio(cls, v):
        if not v.strip():
            raise ValueError("El concepto no puede estar vacío")
        return v