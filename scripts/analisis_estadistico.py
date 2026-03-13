# Script para ver qué onda con los datos que hemos sacado
# Quiero ver si la altitud de la ISS cambia mucho o si es estable

import pandas as pd
import matplotlib.pyplot as plt

def analizar_datos():
    ruta = "data/dataset_iss_24h.csv"
    df = pd.read_csv(ruta)

    # Saco los datos básicos (Media, Min, Max)
    # Esto me sirve para el capítulo 5 del TFG
    print("--- Resumen Estadístico de la Altitud (24h) ---")
    print(df['altitud_km'].describe())

    # Voy a dibujar una gráfica para ver si la altura sube o baja
    plt.figure(figsize=(10, 5))
    plt.plot(df['altitud_km'], color='red', label='Altitud Real (SGP4)')
    plt.title('Variación de la Altitud de la ISS en 24 Horas')
    plt.xlabel('Minutos transcurridos')
    plt.ylabel('Kilómetros')
    plt.grid(True)
    plt.legend()
    
    # La guardo en la carpeta de resultados para enseñársela al profe
    plt.savefig('results/analisis_altitud.png')
    print("\nGráfica guardada en results/analisis_altitud.png")
    plt.show()

if __name__ == "__main__":
    analizar_datos()

# He sacado este dibujo para ver si los datos de la ISS tenían sentido.
# Lo que se ve son "montañas" que suben y bajan; cada montaña es una vuelta a la Tierra (una órbita).
# Me sirve para demostrar que la ISS no va en línea recta, sino que su altura cambia 
# un poco por la forma de la Tierra y el aire que la frena.
# Si la gráfica sale así, es que el dataset de 24h está bien generado y puedo seguir.