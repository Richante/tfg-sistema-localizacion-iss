# Script para comparar lo que calcula SGP4 con la referencia OEM de NASA.
# Guardo las posiciones de ambos metodos y el error en kilometros para entrenar la IA.

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from skyfield.api import EarthSatellite, load


RUTA_TLE = Path("data/iss_tle_actual.txt")
RUTA_OEM = Path("data/ISS.OEM_J2K_EPH.txt")
RUTA_SALIDA = Path("data/comparacion_sgp4_oem.csv")


def _parsear_fecha_oem(valor: str) -> datetime:
    # NASA puede publicar la fecha en formato calendario o con dia del anio.
    limpio = valor.strip().replace("Z", "")
    formatos = (
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%jT%H:%M:%S.%f",
        "%Y-%jT%H:%M:%S",
    )

    for formato in formatos:
        try:
            return datetime.strptime(limpio, formato).replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    raise ValueError(f"Formato de fecha OEM no soportado: {valor}")


def cargar_oem(ruta_oem: Path = RUTA_OEM) -> pd.DataFrame:
    if not ruta_oem.exists():
        raise FileNotFoundError(
            f"No existe {ruta_oem}. Ejecuta primero scripts/descargar_oem_nasa.py"
        )

    filas = []
    for linea in ruta_oem.read_text(encoding="utf-8").splitlines():
        partes = linea.split()

        if len(partes) < 7 or not partes[0][:4].isdigit():
            continue

        try:
            fecha = _parsear_fecha_oem(partes[0])
            valores = [float(valor) for valor in partes[1:7]]
        except ValueError:
            continue

        filas.append(
            {
                "fecha_hora": fecha,
                "oem_x_km": valores[0],
                "oem_y_km": valores[1],
                "oem_z_km": valores[2],
                "oem_vx_km_s": valores[3],
                "oem_vy_km_s": valores[4],
                "oem_vz_km_s": valores[5],
            }
        )

    if not filas:
        raise ValueError(f"No se han encontrado vectores de estado en {ruta_oem}")

    return pd.DataFrame(filas).sort_values("fecha_hora").reset_index(drop=True)


def cargar_satelite_desde_tle(ruta_tle: Path = RUTA_TLE) -> EarthSatellite:
    if not ruta_tle.exists():
        raise FileNotFoundError(f"No existe {ruta_tle}")

    lineas = [
        linea.strip()
        for linea in ruta_tle.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]

    for indice in range(len(lineas) - 2):
        nombre, linea1, linea2 = lineas[indice : indice + 3]
        if nombre.startswith("ISS") and linea1.startswith("1 ") and linea2.startswith("2 "):
            ts = load.timescale()
            return EarthSatellite(linea1, linea2, nombre, ts)

    raise ValueError("No se ha encontrado un TLE valido de la ISS")


def propagar_sgp4(timestamps: pd.Series, satelite: EarthSatellite) -> pd.DataFrame:
    ts = load.timescale()
    posiciones = []

    for fecha in timestamps:
        momento = fecha.to_pydatetime() if hasattr(fecha, "to_pydatetime") else fecha
        momento = momento.astimezone(timezone.utc)
        t = ts.utc(
            momento.year,
            momento.month,
            momento.day,
            momento.hour,
            momento.minute,
            momento.second + momento.microsecond / 1_000_000,
        )
        geocentrico = satelite.at(t)
        x_km, y_km, z_km = geocentrico.position.km
        vx_km_s, vy_km_s, vz_km_s = geocentrico.velocity.km_per_s
        posiciones.append(
            {
                "sgp4_x_km": x_km,
                "sgp4_y_km": y_km,
                "sgp4_z_km": z_km,
                "sgp4_vx_km_s": vx_km_s,
                "sgp4_vy_km_s": vy_km_s,
                "sgp4_vz_km_s": vz_km_s,
            }
        )

    return pd.DataFrame(posiciones)


def comparar_sgp4_oem(
    ruta_oem: Path = RUTA_OEM,
    ruta_tle: Path = RUTA_TLE,
    ruta_salida: Path = RUTA_SALIDA,
) -> pd.DataFrame:
    oem = cargar_oem(ruta_oem)
    satelite = cargar_satelite_desde_tle(ruta_tle)
    sgp4 = propagar_sgp4(oem["fecha_hora"], satelite)

    df = pd.concat([oem, sgp4], axis=1)
    df["residuo_x_km"] = df["oem_x_km"] - df["sgp4_x_km"]
    df["residuo_y_km"] = df["oem_y_km"] - df["sgp4_y_km"]
    df["residuo_z_km"] = df["oem_z_km"] - df["sgp4_z_km"]
    df["error_sgp4_km"] = np.sqrt(
        df["residuo_x_km"] ** 2 + df["residuo_y_km"] ** 2 + df["residuo_z_km"] ** 2
    )

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_salida, index=False)

    print(f"Comparacion guardada en: {ruta_salida}")
    print(f"Vectores comparados: {len(df)}")
    print(f"Error medio SGP4 vs OEM: {df['error_sgp4_km'].mean():.3f} km")
    print(f"Error maximo SGP4 vs OEM: {df['error_sgp4_km'].max():.3f} km")
    return df


if __name__ == "__main__":
    comparar_sgp4_oem()
