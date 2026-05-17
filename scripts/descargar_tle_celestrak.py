"""Descarga el TLE actual de la ISS desde CelesTrak."""

from pathlib import Path

import requests


URL_TLE = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"


def descargar_tle(ruta_salida: str = "data/iss_tle_actual.txt") -> Path:
    salida = Path(ruta_salida)
    salida.parent.mkdir(parents=True, exist_ok=True)

    respuesta = requests.get(URL_TLE, timeout=30)
    respuesta.raise_for_status()
    salida.write_text(respuesta.text, encoding="utf-8")

    print(f"TLE actualizado guardado en: {salida}")
    return salida


if __name__ == "__main__":
    descargar_tle()
