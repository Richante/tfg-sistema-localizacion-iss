# Script para convertir los datos del backend (CSV) al frontend (JSON)
# A esto en ingeniería de software se le llama DTO (Data Transfer Object).

import pandas as pd
import json
import os

def preparar_datos_web():
    ruta_csv = "data/dataset_iss_24h.csv"
    ruta_json = "data/web_visualization.json"

    if not os.path.exists(ruta_csv):
        print("Error: No encuentro el CSV con los datos de la NASA.")
        return

    # 1. Leemos el archivo grande
    df = pd.read_csv(ruta_csv)
    
    # 2. Extraemos solo lo que el mapa necesita (Latitud y Longitud)
    # No mandamos todo el CSV a la web para que cargue ultra rápido
    datos_ligeros = df[['latitud', 'longitud']].to_dict(orient='records')

    # 3. Lo guardamos en formato JSON
    with open(ruta_json, 'w') as archivo:
        json.dump(datos_ligeros, archivo)

    print(f"Datos exportados con éxito a {ruta_json}")

if __name__ == "__main__":
    preparar_datos_web()