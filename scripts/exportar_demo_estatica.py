import json
import shutil
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"
DOCS_DIR = BASE_DIR / "docs"
STATIC_DIR = FRONTEND_DIR / "static"
DOCS_STATIC_DIR = DOCS_DIR / "static"


def leer_json(ruta):
    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def escribir_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def resumen_resultados(ruta_csv):
    df = pd.read_csv(ruta_csv)
    error_sgp4 = float(df["error_sgp4_km"].mean())
    error_ia = float(df["error_ia_km"].mean())
    mejora = ((error_sgp4 - error_ia) / error_sgp4) * 100

    return {
        "error_sgp4_km": round(error_sgp4, 3),
        "error_ia_km": round(error_ia, 3),
        "mejora_porcentaje": round(mejora, 2),
        "muestras": int(len(df)),
    }


def exportar_estado():
    return {
        "servicio": "Demo estatica ISS IA",
        "estado": "ok",
        "modo": "estatico",
        "endpoints": [
            "static/trayectoria.json",
            "static/resultados.json",
            "static/trayectorias-comparadas.json",
        ],
    }


def exportar_resultados():
    ruta_temporal = BASE_DIR / "results" / "evaluacion_corrector_ia_temporal.csv"
    ruta_calibracion = BASE_DIR / "results" / "evaluacion_corrector_ia_calibracion.csv"

    return {
        "temporal": {
            "titulo": "Prediccion de tramo futuro",
            "descripcion": "Entrena con el primer 75% y prueba con datos posteriores.",
            **resumen_resultados(ruta_temporal),
        },
        "calibracion": {
            "titulo": "Calibracion con datos NASA OEM",
            "descripcion": "Entrena y prueba con puntos intercalados dentro de la ventana OEM.",
            **resumen_resultados(ruta_calibracion),
        },
    }


def exportar_trayectorias_comparadas():
    ruta_calibracion = BASE_DIR / "results" / "evaluacion_corrector_ia_calibracion.csv"
    df = pd.read_csv(ruta_calibracion)

    paso = max(1, len(df) // 400)
    df = df.iloc[::paso].copy()

    columnas = [
        "fecha_hora",
        "oem_x_km",
        "oem_y_km",
        "oem_z_km",
        "sgp4_x_km",
        "sgp4_y_km",
        "sgp4_z_km",
        "ia_x_km",
        "ia_y_km",
        "ia_z_km",
        "error_sgp4_km",
        "error_ia_km",
    ]

    df = df[columnas].where(pd.notnull(df[columnas]), None)
    return df.to_dict(orient="records")


def copiar_frontend_a_docs():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for nombre in ("index.html", "style.css", "app.js"):
        shutil.copy2(FRONTEND_DIR / nombre, DOCS_DIR / nombre)

    DOCS_STATIC_DIR.mkdir(parents=True, exist_ok=True)
    for ruta in STATIC_DIR.glob("*.json"):
        shutil.copy2(ruta, DOCS_STATIC_DIR / ruta.name)


def main():
    trayectoria = leer_json(BASE_DIR / "data" / "web_visualization.json")

    escribir_json(STATIC_DIR / "estado.json", exportar_estado())
    escribir_json(STATIC_DIR / "trayectoria.json", trayectoria)
    escribir_json(STATIC_DIR / "resultados.json", exportar_resultados())
    escribir_json(STATIC_DIR / "trayectorias-comparadas.json", exportar_trayectorias_comparadas())
    copiar_frontend_a_docs()

    print("Demo estatica exportada en frontend/static y docs/static")


if __name__ == "__main__":
    main()
