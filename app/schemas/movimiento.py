from pydantic import BaseModel
from datetime import datetime

class MovimientoBase(BaseModel):
    tipo: str
    cantidad: float
    fecha: datetime

    class Config:
        from_attributes = True

class MovimientoCreate(MovimientoBase):
    pass

class MovimientoRead(MovimientoBase):
    id: int
