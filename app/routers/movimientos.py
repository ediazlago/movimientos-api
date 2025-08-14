from fastapi import APIRouter, UploadFile
import pandas as pd
from io import BytesIO
from app.database import SessionLocal
from app.models import MovBancario

router = APIRouter()

@router.post("/cargar_movimientos/")
async def cargar_movimientos(file: UploadFile):
    df = pd.read_excel(BytesIO(await file.read()))
    db = SessionLocal()
    for _, row in df.iterrows():
        movimiento = MovBancario(
            fecha=pd.to_datetime(row['fecha']),
            concepto=row['concepto'],
            fecha_valor=pd.to_datetime(row['fecha valor']),
            importe=row['importe'],
            saldo=row['saldo']
        )
        db.add(movimiento)
    db.commit()
    db.close()
    return {"mensaje": "Movimientos cargados correctamente"}
