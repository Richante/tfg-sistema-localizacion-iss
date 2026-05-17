# Script para dejar los datos preparados para la IA.
# Normalizo latitud, longitud y altitud para que el modelo trabaje con valores parecidos.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

def preparar_datos():
    ruta_entrada = "data/dataset_iss_24h.csv"
    ruta_salida = "data/dataset_ia_listo.csv"
    
    if not os.path.exists(ruta_entrada):
        print("Error: No encuentro el CSV de 24h!")
        return
        
    df = pd.read_csv(ruta_entrada)
    
    # Me quedo solo con las variables que voy a usar para entrenar.
    datos_limpios = df[['latitud', 'longitud', 'altitud_km']]
    
    # Escalo los valores entre 0 y 1 para que ninguna variable pese demasiado.
    scaler = MinMaxScaler()
    datos_escalados = scaler.fit_transform(datos_limpios)
    
    # Guardo el resultado para el entrenamiento.
    df_final = pd.DataFrame(datos_escalados, columns=['lat', 'lon', 'alt'])
    df_final.to_csv(ruta_salida, index=False)
    
    print("Datos normalizados y listos en data/dataset_ia_listo.csv")
    print("He usado MinMaxScaler para que todos los valores estén entre 0 y 1.")

if __name__ == "__main__":
    preparar_datos()

# Nota para la memoria:
# la Regresion Lineal sirve como modelo base, pero Random Forest se adapta mejor
# a una trayectoria con curvas y ciclos repetidos como la de la ISS.
