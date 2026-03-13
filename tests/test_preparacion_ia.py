# Test para asegurar que la comida de la IA está bien preparada
# Quiero que los datos existan y que estén escalados entre 0 y 1

import pandas as pd
import os

def test_datos_normalizados():
    ruta = "data/dataset_ia_listo.csv"
    
    # Esto fallará primero porque el archivo no existe
    assert os.path.exists(ruta), "El dataset para la IA no ha sido generado."
    
    df = pd.read_csv(ruta)
    
    # Compruebo que no haya valores mayores que 1 ni menores que 0
    # Si esto falla, es que la normalización se hizo mal
    assert (df >= 0).all().all() and (df <= 1).all().all(), "Los datos no están entre 0 y 1!"
    
    print("✅ Test de normalización pasado: los datos son aptos para la IA.")

if __name__ == "__main__":
    test_datos_normalizados()