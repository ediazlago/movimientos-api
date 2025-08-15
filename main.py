# main.py
from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.database import Base, engine, verificar_conexion
from app.routes.movimientos import router as movimientos_router
import pandas as pd
import os

# Cargar variables del entorno
load_dotenv()

# Configuración básica
DEBUG = os.getenv("DEBUG") == "True"
PORT = int(os.getenv("PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Inicializar la app
app = FastAPI()

# Verificar conexión y crear tablas
verificar_conexion()
Base.metadata.create_all(bind=engine)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(movimientos_router, prefix="/api/movimientos")

# Columnas esperadas en el Excel
COLUMNAS_ESPERADAS = ["fecha", "concepto", "fechavalor", "importe", "saldo"]
df_cache = {}

@app.get("/", response_class=HTMLResponse)
def formulario_subida():
    return """
    <html>
        <head><title>Subir Excel</title></head>
        <body>
            <h2>Sube tu archivo Excel</h2>
            <form action="/vista-previa" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept=".xlsx"/>
                <input type="submit" value="Ver vista previa"/>
            </form>
        </body>
    </html>
    """

@app.post("/vista-previa")
async def vista_previa(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(contents, engine="openpyxl")

    columnas_recibidas = list(df.columns)
    faltantes = [col for col in COLUMNAS_ESPERADAS if col not in columnas_recibidas]

    if faltantes:
        return HTMLResponse(
            content=f"<h3>Error: Faltan columnas obligatorias: {', '.join(faltantes)}</h3>",
            status_code=400
        )

    df_cache["preview"] = df.head(5)

    # Generar formulario editable
    html = "<h3>Edita los datos antes de insertar</h3>"
    html += '<form action="/confirmar-insercion" method="post">'
    html += '<table border="1"><tr>'
    for col in COLUMNAS_ESPERADAS:
        html += f"<th>{col}</th>"
    html += "</tr>"

    for i, row in df_cache["preview"].iterrows():
        html += "<tr>"
        for col in COLUMNAS_ESPERADAS:
            valor = row[col]
            html += f'<td><input type="text" name="{col}_{i}" value="{valor}"/></td>'
        html += "</tr>"

    html += "</table><br>"
    html += '<input type="submit" value="Confirmar e insertar"/>'
    html += "</form>"

    return HTMLResponse(content=html)

@app.post("/confirmar-insercion")
async def confirmar_insercion(request: Request):
    form_data = await request.form()
    df = df_cache.get("preview")
    if df is None:
        return HTMLResponse(content="<h3>Error: No hay datos para insertar.</h3>", status_code=400)

    nuevos_datos = []
    for i in range(len(df)):
        fila = {}
        for col in COLUMNAS_ESPERADAS:
            clave = f"{col}_{i}"
            fila[col] = form_data.get(clave)
        nuevos_datos.append(fila)

    df_editado = pd.DataFrame(nuevos_datos)

    # Validación básica
    try:
        df_editado["fecha"] = pd.to_datetime(df_editado["fecha"])
        df_editado["fechavalor"] = pd.to_datetime(df_editado["fechavalor"])
        df_editado["importe"] = pd.to_numeric(df_editado["importe"])
        df_editado["saldo"] = pd.to_numeric(df_editado["saldo"])
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error en la validación de datos: {str(e)}</h3>", status_code=400)

    df_editado.to_sql(name="MovBancarios", con=engine, if_exists="append", index=False)
    df_cache.clear()

    return HTMLResponse(content=f"<h3>{len(df_editado)} filas insertadas correctamente.</h3>")

# Ejecutar la app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=DEBUG)