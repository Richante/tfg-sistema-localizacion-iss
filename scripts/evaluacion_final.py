# Script para hacer una evaluacion final sencilla del modelo guardado.
# Comparo la prediccion de la IA con los datos que ya tenia preparados.

import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error
import os

def evaluar_sistema():
    ruta_datos = "data/dataset_ia_listo.csv"
    ruta_modelo = "models/modelo_iss.joblib"

    if not os.path.exists(ruta_modelo):
        print("Error: No encuentro el modelo de la IA (.joblib).")
        return

    # Cargo el modelo guardado y los datos preparados.
    modelo_ia = joblib.load(ruta_modelo)
    df = pd.read_csv(ruta_datos)

    # Uso los ultimos 100 puntos como una prueba simple.
    datos_prueba = df.tail(100)
    
    # Lo que sabemos: el estado actual.
    X_prueba = datos_prueba[['lat', 'lon', 'alt']].iloc[:-1]
    # Lo que queremos estimar: el siguiente minuto real.
    y_real = datos_prueba[['lat', 'lon', 'alt']].iloc[1:]

    # La IA calcula su prediccion.
    prediccion_ia = modelo_ia.predict(X_prueba)

    # Calculo el error medio de la IA en cada coordenada.
    error_ia_lat = mean_absolute_error(y_real['lat'], prediccion_ia[:, 0])
    error_ia_lon = mean_absolute_error(y_real['lon'], prediccion_ia[:, 1])
    error_ia_alt = mean_absolute_error(y_real['alt'], prediccion_ia[:, 2])

    print("=== RESULTADOS DE LA EVALUACIÓN FINAL ===")
    print("Error medio de la IA al predecir el siguiente minuto (datos normalizados):")
    print(f"Latitud:  {error_ia_lat:.6f}")
    print(f"Longitud: {error_ia_lon:.6f}")
    print(f"Altitud:  {error_ia_alt:.6f}")
    
    print("\nConclusion para el TFG:")
    print("Los errores bajos indican que Random Forest puede seguir bien")
    print("la trayectoria cuando se entrena con datos ya preparados.")
    print("Esta prueba sirve como apoyo antes de la validacion con NASA OEM.")

if __name__ == "__main__":
    evaluar_sistema()
