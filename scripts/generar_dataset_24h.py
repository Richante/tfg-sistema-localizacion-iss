# Script para sacar un montón de datos de la ISS y no solo una hora
# Lo hago para tener un CSV grande y que la IA tenga de donde aprender

import pandas as pd
from datetime import datetime, timedelta
from skyfield.api import load, EarthSatellite
import os

def ejecutar_generacion():
    # Busco las rutas de los archivos para no liarme con las carpetas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_tle = os.path.join(base_dir, '../data/iss_tle.txt')
    ruta_salida = os.path.join(base_dir, '../data/dataset_iss_24h.csv')

    # Creo la carpeta data si no existe, por si acaso
    if not os.path.exists(os.path.join(base_dir, '../data')):
        os.makedirs(os.path.join(base_dir, '../data'))

    # Miro si el TLE de la NASA está ahí
    if not os.path.exists(ruta_tle):
        print("Oye, falta el iss_tle.txt en la carpeta data. Descárgalo primero!")
        return

    # Leo las líneas del TLE para pasárselas al motor de Skyfield
    with open(ruta_tle, 'r') as f:
        lineas = f.readlines()
    
    nombre = lineas[0].strip()
    linea1 = lineas[1].strip()
    linea2 = lineas[2].strip()

    ts = load.timescale()
    satelite = EarthSatellite(linea1, linea2, nombre, ts)
    
    # Me guardo el BSTAR porque el profe dijo que era importante para el rozamiento
    bstar = satelite.model.bstar 

    print(f"Empezando a calcular puntos para: {nombre}...")
    datos = []
    ahora = datetime.utcnow()

    # Voy a sacar 1440 puntos (uno por cada minuto de un día entero)
    for i in range(1440):
        momento_utc = ahora - timedelta(minutes=i)
        t = ts.utc(momento_utc.year, momento_utc.month, momento_utc.day, 
                   momento_utc.hour, momento_utc.minute, momento_utc.second)
        
        # Calculo la posición usando SGP4
        geocentrico = satelite.at(t)
        subpunto = geocentrico.subpoint()

        datos.append({
            "fecha_hora": momento_utc.isoformat(),
            "latitud": subpunto.latitude.degrees,
            "longitud": subpunto.longitude.degrees,
            "altitud_km": subpunto.elevation.km,
            "bstar_nasa": bstar
        })

    # Lo paso a un DataFrame y lo guardo
    df = pd.DataFrame(datos)
    df.to_csv(ruta_salida, index=False)
    print(f"Listo! He guardado {len(df)} filas en el CSV nuevo.")

if __name__ == "__main__":
    ejecutar_generacion()