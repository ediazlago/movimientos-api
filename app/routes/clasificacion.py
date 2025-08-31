# app/routes/clasificacion.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/clasificacion")

@router.get("/", response_class=HTMLResponse)
def clasificacion(request: Request):
    return """
    <html>
    <head><title>Clasificación de Gastos</title></head>
    <body>
        <h1>📝 Clasificación de Gastos</h1>
        <p>Aquí podrás clasificar tus movimientos bancarios.</p>
        <a href="/proxy/8000/">Volver al Dashboard Principal</a>
    </body>
    </html>
    """
