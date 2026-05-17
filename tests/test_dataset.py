# Test para comprobar que el CSV de 24 horas se ha generado bien.
# Asi evito entrenar la IA con datos incompletos o fuera de rango.

import pandas as pd
import os

def test_calidad_datos():
    # Compruebo que el archivo existe en la ruta esperada.
    ruta = "data/dataset_iss_24h.csv"
    
    print(f"Comprobando archivo: {ruta}")
    assert os.path.exists(ruta), "Error: No encuentro el CSV de 24h!"
    
    df = pd.read_csv(ruta)
    
    # Debe tener 1440 filas: una por cada minuto del dia.
    assert len(df) == 1440, f"faltan datos. Hay {len(df)} filas."
    
    # Compruebo que las coordenadas no se salen del rango del mapa.
    assert df['latitud'].between(-90, 90).all(), "Hay una latitud rara fuera de rango."
    assert df['longitud'].between(-180, 180).all(), "Hay una longitud fuera de rango."
    
    # Miro que no haya huecos vacios que luego afecten al entrenamiento.
    assert not df.isnull().values.any(), "Hay valores nulos en el dataset."
    
    print("Todo parece correcto, Los datos están limpios y listos.")

if __name__ == "__main__":
    # Permite ejecutar este archivo directamente si necesito probarlo a mano.
    test_calidad_datos()
