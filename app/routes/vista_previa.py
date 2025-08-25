# app/routes/vista_previa.py
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from app.utils.excel import leer_excel_con_encabezados, COLUMNAS_ESPERADAS
from app.models.movimiento import Movimiento
from app.database import engine
import pandas as pd
import json
from io import BytesIO

router = APIRouter()
df_cache = {}

@router.get("/", response_class=HTMLResponse)
def formulario_subida():
    df_cache.clear()
    return """
    <html>
    <head><title>Subir Excel</title></head>
    <body>
    <h2>Sube tu archivo Excel</h2>
    <form action="vista-previa" enctype="multipart/form-data" method="post">
        <input name="file" type="file" accept=".xls,.xlsx"/>
        <input type="submit" value="Ver vista previa"/>
    </form>
    </body>
    </html>
    """

@router.post("/vista-previa")
async def vista_previa(file: UploadFile = File(...)):
    filename = file.filename.lower().strip()
    if not filename.endswith((".xlsx", ".xls")):
        return HTMLResponse(
            content="<h3>Error: El archivo debe tener extensión .xlsx o .xls</h3>",
            status_code=400
        )

    contents = await file.read()
    df = leer_excel_con_encabezados(BytesIO(contents), filename)
    if isinstance(df, HTMLResponse):
        return df

    # Comprobar columnas obligatorias
    columnas_recibidas = list(df.columns)
    faltantes = [col for col in COLUMNAS_ESPERADAS if col not in columnas_recibidas]
    if faltantes:
        return HTMLResponse(
            content=f"<h3>Error: Faltan columnas obligatorias: {', '.join(faltantes)}</h3>",
            status_code=400
        )

    # Convertir fechas a datetime
    for col in ["fecha_operacion", "fecha_valor"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # Filtrar filas inválidas
    df_preview = df.copy()
    df_preview = df_preview[
        df_preview["concepto"].notna() & df_preview["concepto"].str.strip().astype(bool) &
        pd.to_numeric(df_preview["importe"], errors="coerce").notna() &
        pd.to_numeric(df_preview["saldo"], errors="coerce").notna()
    ].reset_index(drop=True)

    df_cache["preview"] = df_preview

    # Convertir Timestamp a string para JSON
    df_preview_serializable = df_preview.copy()
    for col in ["fecha_operacion", "fecha_valor"]:
        if col in df_preview_serializable.columns:
            df_preview_serializable[col] = df_preview_serializable[col].dt.strftime("%d/%m/%Y")

    datos_json_str = json.dumps(df_preview_serializable.to_dict(orient="records"), ensure_ascii=False)\
        .replace("\\", "\\\\").replace('"', '\\"')
    columnas_json_str = json.dumps(COLUMNAS_ESPERADAS, ensure_ascii=False)\
        .replace("\\", "\\\\").replace('"', '\\"')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Vista previa</title>
    <script>
    const datos = JSON.parse("{datos_json_str}");
    const columnas = JSON.parse("{columnas_json_str}");

    window.onload = function() {{
        let html = "<table border='1'><tr>";
        for (const col of columnas) {{ html += `<th>${{col}}</th>`; }}
        html += "</tr>";
        datos.forEach((fila, i) => {{
            html += "<tr>";
            for (const col of columnas) {{
                const valor = fila[col] || "";
                html += `<td><input type='text' name='${{col}}_${{i}}' value='${{valor}}'/></td>`;
            }}
            html += "</tr>";
        }});
        html += "</table>";
        document.getElementById("tabla").innerHTML = html;
    }}
    </script>
    </head>
    <body>
    <h3>Edita los datos antes de insertar</h3>
    <form action="confirmar-insercion" method="post">
        <div id="tabla">Cargando vista previa...</div>
        <br>
        <input type="submit" value="Confirmar e insertar"/>
    </form>
    <br>
    <form action="/proxy/8000/cancelar" method="get">
        <input type="submit" value="Cancelar"/>
    </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/cancelar", response_class=HTMLResponse)
def cancelar():
    df_cache.clear()
    return """
    <html>
    <head>
    <meta http-equiv="refresh" content="0; url=https://visual.edl1989.es/proxy/8000/" />
    </head>
    <body>
    <p>Redirigiendo...</p>
    </body>
    </html>
    """

@router.post("/confirmar-insercion")
async def confirmar_insercion(request: Request):
    form_data = await request.form()
    df = df_cache.get("preview")
    if df is None or df.empty:
        return HTMLResponse(content="<h3>Error: No hay datos válidos para insertar.</h3>", status_code=400)

    nuevos_datos = []
    for i in range(len(df)):
        fila = {}
        for col in COLUMNAS_ESPERADAS:
            clave = f"{col}_{i}"
            fila[col] = form_data.get(clave)
        nuevos_datos.append(fila)

    df_editado = pd.DataFrame(nuevos_datos)
    df_editado = df_editado.applymap(lambda x: str(x).strip() if pd.notnull(x) else x)

    # Renombrar columnas si es necesario
    df_editado = df_editado.rename(columns={"fecha valor": "fecha_valor", "fecha": "fecha_operacion"})

    # Convertir fechas
    for col in ["fecha_operacion", "fecha_valor"]:
        if col in df_editado.columns:
            df_editado[col] = pd.to_datetime(df_editado[col], errors="coerce", dayfirst=True)

    # Convertir importes y saldo a float
    for col in ["importe", "saldo"]:
        if col in df_editado.columns:
            df_editado[col] = pd.to_numeric(df_editado[col], errors="coerce")

    # Filtrar filas inválidas antes de validación
    df_editado = df_editado[
        df_editado["concepto"].notna() & df_editado["concepto"].str.strip().astype(bool) &
        df_editado["importe"].notna() &
        df_editado["saldo"].notna()
    ].reset_index(drop=True)

    # Validación con Pydantic
    errores = []
    datos_validados = []
    for i, row in df_editado.iterrows():
        try:
            movimiento = Movimiento(**row)
            datos_validados.append(movimiento.dict())
        except Exception as e:
            errores.append(f"<li>Fila {i+1}: {str(e)}</li>")

    if errores:
        return HTMLResponse(
            content=f"<h3>Errores de validación:</h3><ul>{''.join(errores)}</ul>"
                    f"<form action='/proxy/8000/cancelar' method='get'>"
                    f"<input type='submit' value='Cancelar'/></form>",
            status_code=400
        )

    # Insertar en la base de datos
    df_validado = pd.DataFrame(datos_validados)
    df_validado.to_sql(name="MovBancarios", con=engine, if_exists="append", index=False)
    df_cache.clear()

    return HTMLResponse(
        content=f"<h3>{len(df_validado)} filas insertadas correctamente.</h3>"
                f"<form action='/proxy/8000/' method='get'>"
                f"<input type='submit' value='Volver al inicio'/></form>"
    )
