# app/utils/excel.py
import pandas as pd
from fastapi.responses import HTMLResponse

COLUMNAS_ESPERADAS = ["fecha", "concepto", "fecha valor", "importe", "saldo"]

def leer_excel_con_encabezados(contents, filename):
    try:
        extension = filename.lower().split(".")[-1]
        engine = "openpyxl" if extension == "xlsx" else "xlrd"

        temp_df = pd.read_excel(contents, engine=engine, header=None)
        for i, row in temp_df.iterrows():
            columnas = [str(cell).strip().lower() for cell in row]
            if all(col.lower() in columnas for col in COLUMNAS_ESPERADAS):
                df = pd.read_excel(contents, engine=engine, skiprows=i)
                df = df.dropna(how="all")
                return df

        return HTMLResponse(
            content="<h3>Error: No se encontraron las columnas esperadas en el archivo.</h3>",
            status_code=400
        )
    except Exception as e:
        return HTMLResponse(
            content=f"<h3>Error al leer el archivo: {str(e)}</h3>",
            status_code=500
        )
