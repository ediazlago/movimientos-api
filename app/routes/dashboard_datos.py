# app/routes/dashboard_datos.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/dashboard-datos")

@router.get("/", response_class=HTMLResponse)
def dashboard_datos(request: Request):
    return """
    <html>
    <head><title>Dashboard de Datos</title></head>
    <body>
        <h1>📊 Dashboard de Datos</h1>
        <p>Aquí se mostrarán tus datos y estadísticas.</p>
        <a href="/proxy/8000/">Volver al Dashboard Principal</a>
    </body>
    </html>
    """
