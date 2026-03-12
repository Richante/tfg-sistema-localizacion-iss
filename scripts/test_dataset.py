# Mi primer test de TDD para el TFG
# Ahora mismo va a fallar porque el CSV de 24h no existe todavía

import os
import pandas as pd

def test_existencia_dataset():
    # Solo quiero ver si el archivo está ahí
    ruta = "data/dataset_iss_24h.csv"
    
    print(f"Buscando el archivo en: {ruta}")
    
    # Esta línea va a dar error (AssertionError) si el archivo no existe
    assert os.path.exists(ruta), "El archivo de 24h no existe, el test falla!"

if __name__ == "__main__":
    test_calidad_datos()