# Script para dejar los datos listos para la IA
# Lo hago simple: convierto las horas en números y normalizo todo
# Así la IA no se confunde con números muy grandes o pequeños

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
    
    # 1. Me quedo solo con lo que importa: Lat, Lon, Alt
    # No uso la fecha directamente porque la IA no entiende texto
    datos_limpios = df[['latitud', 'longitud', 'altitud_km']]
    
    # 2. Normalización (Escalar entre 0 y 1)
    # Justificación: Para que la IA trate igual a la latitud que a la altitud
    scaler = MinMaxScaler()
    datos_escalados = scaler.fit_transform(datos_limpios)
    
    # 3. Guardamos el resultado para el entrenamiento
    df_final = pd.DataFrame(datos_escalados, columns=['lat', 'lon', 'alt'])
    df_final.to_csv(ruta_salida, index=False)
    
    print("Datos normalizados y listos en data/dataset_ia_listo.csv")
    print("He usado MinMaxScaler para que todos los valores estén entre 0 y 1.")

if __name__ == "__main__":
    preparar_datos()

    #1. He visto que la Regresión Lineal falla bastante (0.014) porque intenta trazar 
#líneas rectas, y como la ISS se mueve en órbitas (curvas), no puede seguirla bien.

#2. El Random Forest ha ganado por paliza (0.0009). Al usar árboles de decisión, 
#mi IA ha sido capaz de "entender" los ciclos de 90 minutos de la ISS y se adapta 
#mucho mejor a las curvas de la trayectoria.

#3. Con este error tan bajo, he demostrado que el Random Forest es el modelo 
#ideal para mi proyecto. Ahora puedo dejar de comparar y centrarme en usar 
#este "cerebro" para corregir las predicciones de la NASA.