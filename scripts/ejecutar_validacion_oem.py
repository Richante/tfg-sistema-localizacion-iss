"""Ejecuta la validacion completa SGP4 vs NASA OEM."""

from comparar_sgp4_oem import comparar_sgp4_oem
from descargar_oem_nasa import descargar_oem
from descargar_tle_celestrak import descargar_tle
from entrenar_corrector_ia import entrenar_corrector


def ejecutar_validacion():
    print("1) Descargando TLE actual desde CelesTrak...")
    descargar_tle()

    print("\n2) Descargando efemeride OEM oficial de NASA...")
    descargar_oem()

    print("\n3) Comparando SGP4 contra NASA OEM...")
    comparar_sgp4_oem()

    print("\n4) Entrenando corrector IA...")
    entrenar_corrector()


if __name__ == "__main__":
    ejecutar_validacion()
