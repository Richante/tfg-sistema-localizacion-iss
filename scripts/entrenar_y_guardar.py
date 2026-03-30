# Script para entrenar al modelo ganador (Random Forest) con TODOS los datos
# y guardarlo en un archivo. Así no tengo que entrenarlo cada vez que lo use.

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def guardar_modelo_definitivo():
    ruta_datos = "data/dataset_ia_listo.csv"
    ruta_modelo = "models/modelo_iss.joblib"
    
    # 1. Por si acaso no existe la carpeta 'models', la creo automáticamente
    os.makedirs("models", exist_ok=True)
    
    if not os.path.exists(ruta_datos):
        print("Falta el archivo listo para IA. Correr el script de preparar_ia primero")
        return

    df = pd.read_csv(ruta_datos)

    # 2. Preparo el entrenamiento:
    # X = Dónde está la ISS ahora (todo menos el último minuto)
    # y = Dónde estará en el siguiente minuto (todo menos el primer minuto)
    X = df[['lat', 'lon', 'alt']].iloc[:-1]
    y = df[['lat', 'lon', 'alt']].iloc[1:]

    # 3. Entreno con TODOS los datos (ya no separo para testear porque ya sé que funciona)
    print("Entrenando el cerebro definitivo (Random Forest)....")
    modelo_final = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_final.fit(X, y)

    # 4. Congelo el cerebro y lo guardo en un archivo
    joblib.dump(modelo_final, ruta_modelo)
    
    print(f"El modelo está guardado y listo para usarse en: {ruta_modelo}")

    
    #Uso 'joblib' porque es el estándar en Python para serializar (guardar) 
    #modelos de Scikit-Learn. Ahora mi web o mi sistema predictivo solo 
    # tiene que cargar este archivo .joblib y hacer la predicción al instante, 
    # sin gastar CPU en reentrenar.

if __name__ == "__main__":
    guardar_modelo_definitivo()