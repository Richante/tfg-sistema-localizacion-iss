"""Descarga la efemeride OEM oficial de la ISS publicada por NASA.

El archivo OEM de Spot the Station se usa como referencia externa para
comparar la prediccion SGP4 basada en TLE con una trayectoria operacional
publicada por NASA/JSC.
"""

from pathlib import Path

import requests


URL_OEM_NASA = (
    "https://nasa-public-data.s3.amazonaws.com/"
    "iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.txt"
)


def descargar_oem(ruta_salida: str = "data/ISS.OEM_J2K_EPH.txt") -> Path:
    salida = Path(ruta_salida)
    salida.parent.mkdir(parents=True, exist_ok=True)

    respuesta = requests.get(URL_OEM_NASA, timeout=30)
    respuesta.raise_for_status()
    salida.write_text(respuesta.text, encoding="utf-8")

    print(f"OEM de NASA descargado en: {salida}")
    print(f"Tamano del archivo: {salida.stat().st_size} bytes")
    return salida


if __name__ == "__main__":
    descargar_oem()
