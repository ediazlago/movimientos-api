from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

Base = declarative_base()

class MovBancario(Base):
    __tablename__ = "MovBancarios"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    concepto = Column(String(255))
    fecha_valor = Column(Date)
    importe = Column(Float)
    saldo = Column(Float)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
