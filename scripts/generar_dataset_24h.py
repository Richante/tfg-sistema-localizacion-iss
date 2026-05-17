# Script para generar un dataset de 24 horas de la ISS.
# Lo uso para tener mas puntos de trayectoria con los que entrenar la IA.

import pandas as pd
from datetime import datetime, timedelta
from skyfield.api import load, EarthSatellite
import os

def ejecutar_generacion():
    # Preparo las rutas de entrada y salida.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_tle = os.path.join(base_dir, '../data/iss_tle.txt')
    ruta_salida = os.path.join(base_dir, '../data/dataset_iss_24h.csv')

    # Creo la carpeta data si todavia no existe.
    if not os.path.exists(os.path.join(base_dir, '../data')):
        os.makedirs(os.path.join(base_dir, '../data'))

    # Compruebo que el TLE base este disponible.
    if not os.path.exists(ruta_tle):
        print("Falta iss_tle.txt en la carpeta data. Descargalo primero.")
        return

    # Leo las lineas del TLE para pasarlas a Skyfield.
    with open(ruta_tle, 'r') as f:
        lineas = f.readlines()
    
    nombre = lineas[0].strip()
    linea1 = lineas[1].strip()
    linea2 = lineas[2].strip()

    ts = load.timescale()
    satelite = EarthSatellite(linea1, linea2, nombre, ts)
    
    # Guardo BSTAR porque esta relacionado con el rozamiento atmosferico.
    bstar = satelite.model.bstar 

    print(f"Empezando a calcular puntos para: {nombre}...")
    datos = []
    ahora = datetime.utcnow()

    # Genero 1440 puntos, uno por cada minuto de un dia.
    for i in range(1440):
        momento_utc = ahora - timedelta(minutes=i)
        t = ts.utc(momento_utc.year, momento_utc.month, momento_utc.day, 
                   momento_utc.hour, momento_utc.minute, momento_utc.second)
        
        # Calculo la posicion usando SGP4 mediante Skyfield.
        geocentrico = satelite.at(t)
        subpunto = geocentrico.subpoint()

        datos.append({
            "fecha_hora": momento_utc.isoformat(),
            "latitud": subpunto.latitude.degrees,
            "longitud": subpunto.longitude.degrees,
            "altitud_km": subpunto.elevation.km,
            "bstar_nasa": bstar
        })

    # Paso la lista a DataFrame y la guardo en CSV.
    df = pd.DataFrame(datos)
    df.to_csv(ruta_salida, index=False)
    print(f"Listo! He guardado {len(df)} filas en el CSV nuevo.")

if __name__ == "__main__":
    ejecutar_generacion()
