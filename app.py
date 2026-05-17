import json
import os

import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
# CORS permite que la web subida a S3 pueda llamar a esta API en EC2.
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def leer_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def error_si_no_existe(ruta):
    if not os.path.exists(ruta):
        return jsonify({"error": f"No encuentro el archivo {ruta}"}), 404
    return None


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


@app.route("/api/trayectoria", methods=["GET"])
def obtener_trayectoria():
    ruta_json = os.path.join(BASE_DIR, "data", "web_visualization.json")

    error = error_si_no_existe(ruta_json)
    if error:
        return error

    return jsonify(leer_json(ruta_json))


@app.route("/api/resultados", methods=["GET"])
def obtener_resultados():
    ruta_temporal = os.path.join(BASE_DIR, "results", "evaluacion_corrector_ia_temporal.csv")
    ruta_calibracion = os.path.join(
        BASE_DIR, "results", "evaluacion_corrector_ia_calibracion.csv"
    )

    for ruta in (ruta_temporal, ruta_calibracion):
        error = error_si_no_existe(ruta)
        if error:
            return error

    return jsonify(
        {
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
    )


@app.route("/api/trayectorias-comparadas", methods=["GET"])
def obtener_trayectorias_comparadas():
    ruta_calibracion = os.path.join(
        BASE_DIR, "results", "evaluacion_corrector_ia_calibracion.csv"
    )

    error = error_si_no_existe(ruta_calibracion)
    if error:
        return error

    df = pd.read_csv(ruta_calibracion)

    # Envio una muestra para que el navegador cargue rapido.
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

    return jsonify(df[columnas].to_dict(orient="records"))


@app.route("/api/estado", methods=["GET"])
def obtener_estado():
    return jsonify(
        {
            "servicio": "Backend ISS IA",
            "estado": "ok",
            "endpoints": [
                "/api/trayectoria",
                "/api/resultados",
                "/api/trayectorias-comparadas",
            ],
        }
    )


if __name__ == "__main__":
    # Uso el puerto 80 porque es el puerto HTTP normal en AWS.
    app.run(host="0.0.0.0", port=80)
