# Este script lo he creado para asegurar que el entorno de desarrollo
# sea consistente, especialmente pensando en el futuro despliegue en Ubuntu Server.

import sys
import platform
import pandas as pd
import skyfield

def verificar_entorno():
    print("--- Verificación de Entorno de Ingeniería ---")
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Versión de Python: {sys.version}")
    
    # Compruebo las librerías críticas para mi TFG
    librerias = [("Pandas", pd), ("Skyfield", skyfield)]
    
    for nombre, lib in librerias:
        try:
            print(f"[OK] {nombre} instalado - Versión: {lib.__version__}")
        except Exception as e:
            print(f"[ERROR] Problema con {nombre}: {e}")

if __name__ == "__main__":
    verificar_entorno()