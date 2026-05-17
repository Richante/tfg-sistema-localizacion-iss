# Script para revisar si los datos de 24 horas tienen sentido.
# Me fijo sobre todo en la altitud, porque ayuda a comprobar la orbita.

import pandas as pd
import matplotlib.pyplot as plt

def analizar_datos():
    ruta = "data/dataset_iss_24h.csv"
    df = pd.read_csv(ruta)

    # Saco los datos basicos: media, minimo y maximo.
    # Esto me sirve para comentar el comportamiento de la altitud en el TFG.
    print("--- Resumen Estadístico de la Altitud (24h) ---")
    print(df['altitud_km'].describe())

    # Dibujo una grafica para ver como cambia la altura durante el dia.
    plt.figure(figsize=(10, 5))
    plt.plot(df['altitud_km'], color='red', label='Altitud Real (SGP4)')
    plt.title('Variación de la Altitud de la ISS en 24 Horas')
    plt.xlabel('Minutos transcurridos')
    plt.ylabel('Kilómetros')
    plt.grid(True)
    plt.legend()
    
    # La guardo en resultados para poder usarla en la memoria.
    plt.savefig('results/analisis_altitud.png')
    print("\nGráfica guardada en results/analisis_altitud.png")
    plt.show()

if __name__ == "__main__":
    analizar_datos()

# Esta grafica me ayuda a comprobar que el dataset tiene una forma coherente.
# Las subidas y bajadas se relacionan con las vueltas de la ISS alrededor de la Tierra.
# Si la curva sale estable y sin saltos raros, puedo seguir usando estos datos.
