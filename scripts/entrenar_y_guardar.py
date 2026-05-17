# Script para entrenar el modelo Random Forest con todos los datos disponibles.
# Lo guardo en un archivo para poder reutilizarlo sin entrenarlo cada vez.

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def guardar_modelo_definitivo():
    ruta_datos = "data/dataset_ia_listo.csv"
    ruta_modelo = "models/modelo_iss.joblib"
    
    # Creo la carpeta de modelos si todavia no existe.
    os.makedirs("models", exist_ok=True)
    
    if not os.path.exists(ruta_datos):
        print("Falta el archivo listo para IA. Correr el script de preparar_ia primero")
        return

    df = pd.read_csv(ruta_datos)

    # X representa el estado actual de la ISS.
    # y representa el estado del minuto siguiente.
    X = df[['lat', 'lon', 'alt']].iloc[:-1]
    y = df[['lat', 'lon', 'alt']].iloc[1:]

    # Entreno el modelo final con todos los datos ya preparados.
    print("Entrenando el modelo final (Random Forest)....")
    modelo_final = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_final.fit(X, y)

    # Guardo el modelo entrenado en un archivo .joblib.
    joblib.dump(modelo_final, ruta_modelo)
    
    print(f"El modelo está guardado y listo para usarse en: {ruta_modelo}")

    
    # Uso joblib porque es una forma habitual de guardar modelos de Scikit-Learn.
    # Asi la aplicacion solo tiene que cargar el archivo y hacer la prediccion.

if __name__ == "__main__":
    guardar_modelo_definitivo()
