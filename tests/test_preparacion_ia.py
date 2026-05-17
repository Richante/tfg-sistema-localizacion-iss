# Test para comprobar que los datos de la IA estan bien preparados.
# Deben existir y estar normalizados entre 0 y 1.

import pandas as pd
import os

def test_datos_normalizados():
    ruta = "data/dataset_ia_listo.csv"
    
    # Si el archivo no existe, primero hay que ejecutar scripts/preparar_ia.py.
    assert os.path.exists(ruta), "El dataset para la IA no ha sido generado."
    
    df = pd.read_csv(ruta)
    
    # Compruebo que la normalizacion se ha hecho correctamente.
    assert (df >= 0).all().all() and (df <= 1).all().all(), "Los datos no están entre 0 y 1!"
    
    print("Test de normalizacion pasado: los datos son aptos para la IA.")

if __name__ == "__main__":
    test_datos_normalizados()
