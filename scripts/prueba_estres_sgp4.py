import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import os

def ejecutar_prueba_estres():
    ruta = "data/dataset_ia_listo.csv"
    if not os.path.exists(ruta):
        print("Error: No se encuentra el dataset.")
        return

    df = pd.read_csv(ruta)
    
    X_train = df[['lat', 'lon', 'alt']].iloc[:-1]
    y_train = df['alt'].iloc[1:]
    
    ia_modelo = RandomForestRegressor(n_estimators=50, random_state=42)
    ia_modelo.fit(X_train, y_train)

    # Creo una copia modificable de la altitud para simular una anomalia.
    realidad_altitud = np.array(df['alt'].iloc[:800].copy())
    
    punto_anomalia = 500
    caida_km = 2.0
    realidad_altitud[punto_anomalia:] = realidad_altitud[punto_anomalia:] - caida_km

    prediccion_sgp4 = df['alt'].iloc[:800].values

    prediccion_ia = []
    for i in range(799):
        estado_actual = [[df['lat'].iloc[i], df['lon'].iloc[i], realidad_altitud[i]]]
        siguiente_alt = ia_modelo.predict(estado_actual)[0]
        prediccion_ia.append(siguiente_alt)
    
    prediccion_ia = [realidad_altitud[0]] + prediccion_ia

    plt.figure(figsize=(10, 6))
    plt.plot(realidad_altitud, label='Realidad (Con Tormenta Solar)', color='black', linewidth=3)
    plt.plot(prediccion_sgp4, label='Predicción SGP4 (Ciego / BSTAR Constante)', color='red', linestyle='--', linewidth=2)
    plt.plot(prediccion_ia, label='Predicción IA (Adaptativa)', color='green', linestyle=':', linewidth=3)

    plt.axvline(x=punto_anomalia, color='orange', linestyle='-', alpha=0.5, label='Impacto Tormenta Solar')

    plt.title('Prueba de Estrés: Respuesta a anomalía de altitud (SGP4 vs IA)')
    plt.xlabel('Tiempo (Minutos)')
    plt.ylabel('Altitud (Kilómetros)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('grafica_estres_sgp4_vs_ia.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    ejecutar_prueba_estres()
