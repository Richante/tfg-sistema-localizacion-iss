# Script para ver si el CSV que acabo de crear está bien o si ha salido basura
# Esto es lo que llaman TDD, para no meterle datos malos a la IA

import pandas as pd
import os

def test_calidad_datos():
    # Primero ver si el archivo se ha creado de verdad
    # Uso la ruta relativa desde la raíz del proyecto
    ruta = "data/dataset_iss_24h.csv"
    
    print(f"Comprobando archivo: {ruta}")
    assert os.path.exists(ruta), "Error: No encuentro el CSV de 24h!"
    
    df = pd.read_csv(ruta)
    
    # Chequear que tenga las 1440 filas (las 24 horas)
    assert len(df) == 1440, f"faltan datos. Hay {len(df)} filas."
    
    # Ver si las coordenadas tienen sentido (que no se salgan del mapa)
    assert df['latitud'].between(-90, 90).all(), "Hay una latitud rara fuera de rango."
    assert df['longitud'].between(-180, 180).all(), "La longitud se ha ido de madre."
    
    # Mirar si hay algún hueco vacío (NaN) que luego fastidie la IA
    assert not df.isnull().values.any(), "Hay valores nulos por ahí mezclados."
    
    print("Todo parece correcto, Los datos están limpios y listos.")

if __name__ == "__main__":
    # Llamo a la función correcta para que no de el error de 'not defined'
    test_calidad_datos()