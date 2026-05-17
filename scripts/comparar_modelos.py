# Script para comparar dos modelos sencillos de IA.
# Asi puedo justificar por que uso Random Forest en esta parte del proyecto.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import os

def comparar():
    ruta = "data/dataset_ia_listo.csv"
    if not os.path.exists(ruta):
        print("Falta el archivo listo para IA. Ejecuta primero scripts/preparar_ia.py")
        return

    df = pd.read_csv(ruta)

    # Uso un punto de la trayectoria para intentar predecir la latitud del siguiente.
    X = df[['lat', 'lon', 'alt']].iloc[:-1] # Todos menos el último
    y = df['lat'].iloc[1:]                 # Todos menos el primero (el objetivo)

    # Divido los datos en entrenamiento y prueba.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modelo 1: Regresion Lineal.
    modelo_1 = LinearRegression()
    modelo_1.fit(X_train, y_train)
    pred_1 = modelo_1.predict(X_test)
    error_1 = mean_absolute_error(y_test, pred_1)

    # Modelo 2: Random Forest.
    modelo_2 = RandomForestRegressor(n_estimators=100)
    modelo_2.fit(X_train, y_train)
    pred_2 = modelo_2.predict(X_test)
    error_2 = mean_absolute_error(y_test, pred_2)

    print(f"--- RESULTADOS DEL DUELO ---")
    print(f"Error Regresión Lineal: {error_1:.6f}")
    print(f"Error Random Forest:    {error_2:.6f}")
    
    if error_2 < error_1:
        print("\nGanador: Random Forest. Es más preciso para seguir la ISS.")
    else:
        print("\nGanador: Regresión Lineal. Los datos son más simples de lo que pensaba.")

if __name__ == "__main__":
    comparar()
