from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
