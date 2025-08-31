# app/routes/dashboard.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def dashboard_principal(request: Request):
    return """
    <html>
    <head><title>Dashboard Principal</title></head>
    <body>
        <h1>🏦 Dashboard Principal</h1>
        <ul>
            <li><a href="/proxy/8000/clasificacion/">Clasificación de Gastos</a></li>
            <li><a href="/proxy/8000/vista-previa/">Cargar nuevo Excel</a></li>
            <li><a href="/proxy/8000/dashboard-datos/">Ver Dashboard de Datos</a></li>
        </ul>
    </body>
    </html>
    """
