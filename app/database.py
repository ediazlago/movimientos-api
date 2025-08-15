# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError

# Cargar variables del entorno
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear la base para los modelos
Base = declarative_base()

# Crear una sesión para operaciones con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para verificar la conexión
def verificar_conexion():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos exitosa.")
    except OperationalError as e:
        print("❌ Error al conectar con la base de datos:", e)
