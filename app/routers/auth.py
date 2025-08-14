from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models import Usuario
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/registro/")
def registro(username: str, password: str):
    db = SessionLocal()
    if db.query(Usuario).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    nuevo = Usuario(username=username, hashed_password=hash_password(password))
    db.add(nuevo)
    db.commit()
    db.close()
    return {"mensaje": "Usuario creado"}

@router.post("/login/")
def login(username: str, password: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter_by(username=username).first()
    db.close()
    if not usuario or not verify_password(password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
