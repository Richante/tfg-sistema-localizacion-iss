# Script para ver qué IA es mejor: Regresión simple vs Random Forest
# Así tengo pruebas de por qué elegí una y no otra

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import os

def comparar():
    ruta = "data/dataset_ia_listo.csv"
    if not os.path.exists(ruta):
        print("Falta el archivo listo para IA. ¡Corre el script de preparar_ia primero!")
        return

    df = pd.read_csv(ruta)

    # Queremos predecir la LATITUD basándonos en los puntos anteriores
    # Para hacerlo simple hoy: usamos una fila para predecir la siguiente
    X = df[['lat', 'lon', 'alt']].iloc[:-1] # Todos menos el último
    y = df['lat'].iloc[1:]                 # Todos menos el primero (el objetivo)

    # Divido en 80% para aprender y 20% para examen (test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # MODELO 1: Regresión Lineal
    modelo_1 = LinearRegression()
    modelo_1.fit(X_train, y_train)
    pred_1 = modelo_1.predict(X_test)
    error_1 = mean_absolute_error(y_test, pred_1)