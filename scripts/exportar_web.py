# Script para pasar los datos del CSV a un JSON que pueda leer el frontend.

import pandas as pd
import json
import os

def preparar_datos_web():
    ruta_csv = "data/dataset_iss_24h.csv"
    ruta_json = "data/web_visualization.json"

    if not os.path.exists(ruta_csv):
        print("Error: No encuentro el CSV con los datos de la NASA.")
        return

    # Leo el archivo con la trayectoria.
    df = pd.read_csv(ruta_csv)
    
    # Me quedo solo con latitud y longitud para que el mapa cargue rapido.
    datos_ligeros = df[['latitud', 'longitud']].to_dict(orient='records')

    # Guardo el resultado en formato JSON.
    with open(ruta_json, 'w') as archivo:
        json.dump(datos_ligeros, archivo)

    print(f"Datos exportados con éxito a {ruta_json}")

if __name__ == "__main__":
    preparar_datos_web()
