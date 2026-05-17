"""Entrena una IA correctora del error residual SGP4 -> NASA OEM.

La IA no sustituye a SGP4. Aprende el residuo entre la posicion publicada en
la efemeride OEM de NASA y la posicion calculada con SGP4 para el mismo
timestamp. La prediccion final es:

    posicion_corregida = posicion_sgp4 + residuo_predicho_por_ia
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


RUTA_COMPARACION = Path("data/comparacion_sgp4_oem.csv")
RUTA_MODELO = Path("models/modelo_corrector_sgp4_oem.joblib")
RUTA_RESULTADOS = Path("results/evaluacion_corrector_ia.csv")


FEATURES = [
    "tiempo_min",
    "sgp4_x_km",
    "sgp4_y_km",
    "sgp4_z_km",
    "sgp4_vx_km_s",
    "sgp4_vy_km_s",
    "sgp4_vz_km_s",
]

TARGETS = ["residuo_x_km", "residuo_y_km", "residuo_z_km"]


def _distancia_3d(df: pd.DataFrame, columnas: list[str]) -> pd.Series:
    valores = df[columnas].to_numpy()
    return pd.Series(np.linalg.norm(valores, axis=1), index=df.index)


def entrenar_corrector(
    ruta_comparacion: Path = RUTA_COMPARACION,
    ruta_modelo: Path = RUTA_MODELO,
    ruta_resultados: Path = RUTA_RESULTADOS,
) -> pd.DataFrame:
    if not ruta_comparacion.exists():
        raise FileNotFoundError(
            f"No existe {ruta_comparacion}. Ejecuta primero scripts/comparar_sgp4_oem.py"
        )

    df = pd.read_csv(ruta_comparacion)
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], utc=True)
    df["tiempo_min"] = (df["fecha_hora"] - df["fecha_hora"].min()).dt.total_seconds() / 60
    df = df.dropna(subset=FEATURES + TARGETS)

    X = df[FEATURES]
    y = df[TARGETS]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        shuffle=False,
    )

    modelo = RandomForestRegressor(n_estimators=300, random_state=42)
    modelo.fit(X_train, y_train)

    residuo_predicho = modelo.predict(X_test)
    prueba = df.loc[X_test.index].copy()
    prueba[["ia_residuo_x_km", "ia_residuo_y_km", "ia_residuo_z_km"]] = residuo_predicho

    prueba["ia_x_km"] = prueba["sgp4_x_km"] + prueba["ia_residuo_x_km"]
    prueba["ia_y_km"] = prueba["sgp4_y_km"] + prueba["ia_residuo_y_km"]
    prueba["ia_z_km"] = prueba["sgp4_z_km"] + prueba["ia_residuo_z_km"]

    prueba["error_ia_x_km"] = prueba["oem_x_km"] - prueba["ia_x_km"]
    prueba["error_ia_y_km"] = prueba["oem_y_km"] - prueba["ia_y_km"]
    prueba["error_ia_z_km"] = prueba["oem_z_km"] - prueba["ia_z_km"]
    prueba["error_ia_km"] = _distancia_3d(
        prueba, ["error_ia_x_km", "error_ia_y_km", "error_ia_z_km"]
    )

    mae_sgp4 = mean_absolute_error(
        prueba[["oem_x_km", "oem_y_km", "oem_z_km"]],
        prueba[["sgp4_x_km", "sgp4_y_km", "sgp4_z_km"]],
    )
    mae_ia = mean_absolute_error(
        prueba[["oem_x_km", "oem_y_km", "oem_z_km"]],
        prueba[["ia_x_km", "ia_y_km", "ia_z_km"]],
    )
    mse_sgp4 = mean_squared_error(
        prueba[["oem_x_km", "oem_y_km", "oem_z_km"]],
        prueba[["sgp4_x_km", "sgp4_y_km", "sgp4_z_km"]],
    )
    mse_ia = mean_squared_error(
        prueba[["oem_x_km", "oem_y_km", "oem_z_km"]],
        prueba[["ia_x_km", "ia_y_km", "ia_z_km"]],
    )
    rmse_sgp4 = np.sqrt(mse_sgp4)
    rmse_ia = np.sqrt(mse_ia)

    ruta_modelo.parent.mkdir(parents=True, exist_ok=True)
    ruta_resultados.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, ruta_modelo)
    prueba.to_csv(ruta_resultados, index=False)

    print(f"Modelo corrector guardado en: {ruta_modelo}")
    print(f"Resultados guardados en: {ruta_resultados}")
    print("=== Evaluacion sobre tramo futuro no usado en entrenamiento ===")
    print(f"MAE SGP4:      {mae_sgp4:.3f} km")
    print(f"MAE SGP4 + IA: {mae_ia:.3f} km")
    print(f"RMSE SGP4:      {rmse_sgp4:.3f} km")
    print(f"RMSE SGP4 + IA: {rmse_ia:.3f} km")
    error_3d_sgp4 = prueba["error_sgp4_km"].mean()
    error_3d_ia = prueba["error_ia_km"].mean()

    print(f"Error 3D medio SGP4:      {error_3d_sgp4:.3f} km")
    print(f"Error 3D medio SGP4 + IA: {error_3d_ia:.3f} km")

    if error_3d_ia < error_3d_sgp4:
        print("Conclusion: en este experimento la IA reduce el error de SGP4.")
    else:
        print("Conclusion: en este experimento la IA no mejora a SGP4.")
        print("Esto indica que hacen falta mas datos o variables externas para corregir mejor.")
    return prueba


if __name__ == "__main__":
    entrenar_corrector()
