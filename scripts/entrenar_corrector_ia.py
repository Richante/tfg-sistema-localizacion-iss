# Script para probar si la IA puede corregir parte del error que deja SGP4.
# La idea no es sustituir SGP4, sino aprender la diferencia entre SGP4 y NASA OEM.
# Luego sumo esa correccion a la posicion calculada con SGP4.

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


RUTA_COMPARACION = Path("data/comparacion_sgp4_oem.csv")
RUTA_MODELO = Path("models/modelo_corrector_sgp4_oem.joblib")
RUTA_RESULTADOS_TEMPORAL = Path("results/evaluacion_corrector_ia_temporal.csv")
RUTA_RESULTADOS_CALIBRACION = Path("results/evaluacion_corrector_ia_calibracion.csv")


FEATURES = [
    "tiempo_min",
    "sgp4_x_km",
    "sgp4_y_km",
    "sgp4_z_km",
    "sgp4_vx_km_s",
    "sgp4_vy_km_s",
    "sgp4_vz_km_s",
    "orbita_sin",
    "orbita_cos",
]

TARGETS = ["residuo_x_km", "residuo_y_km", "residuo_z_km"]


def _distancia_3d(df: pd.DataFrame, columnas: list[str]) -> pd.Series:
    valores = df[columnas].to_numpy()
    return pd.Series(np.linalg.norm(valores, axis=1), index=df.index)


def preparar_variables(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], utc=True)
    df["tiempo_min"] = (df["fecha_hora"] - df["fecha_hora"].min()).dt.total_seconds() / 60

    # Meto seno y coseno para que la IA vea que la orbita se repite cada vuelta.
    periodo_orbital_min = 92.95
    angulo = 2 * np.pi * df["tiempo_min"] / periodo_orbital_min
    df["orbita_sin"] = np.sin(angulo)
    df["orbita_cos"] = np.cos(angulo)

    return df.dropna(subset=FEATURES + TARGETS)


def evaluar_modelo(df: pd.DataFrame, train_idx, test_idx, nombre: str) -> pd.DataFrame:
    X_train = df.loc[train_idx, FEATURES]
    y_train = df.loc[train_idx, TARGETS]
    X_test = df.loc[test_idx, FEATURES]

    modelo = RandomForestRegressor(n_estimators=300, random_state=42)
    modelo.fit(X_train, y_train)

    residuo_predicho = modelo.predict(X_test)
    prueba = df.loc[test_idx].copy()
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

    error_3d_sgp4 = prueba["error_sgp4_km"].mean()
    error_3d_ia = prueba["error_ia_km"].mean()

    print(f"=== {nombre} ===")
    print(f"MAE SGP4:      {mae_sgp4:.3f} km")
    print(f"MAE SGP4 + IA: {mae_ia:.3f} km")
    print(f"RMSE SGP4:      {np.sqrt(mse_sgp4):.3f} km")
    print(f"RMSE SGP4 + IA: {np.sqrt(mse_ia):.3f} km")
    print(f"Error 3D medio SGP4:      {error_3d_sgp4:.3f} km")
    print(f"Error 3D medio SGP4 + IA: {error_3d_ia:.3f} km")

    if error_3d_ia < error_3d_sgp4:
        print("Conclusion: en este modo la IA reduce el error de SGP4.\n")
    else:
        print("Conclusion: en este modo la IA no mejora a SGP4.\n")

    return prueba


def entrenar_corrector(
    ruta_comparacion: Path = RUTA_COMPARACION,
    ruta_modelo: Path = RUTA_MODELO,
    ruta_resultados_temporal: Path = RUTA_RESULTADOS_TEMPORAL,
    ruta_resultados_calibracion: Path = RUTA_RESULTADOS_CALIBRACION,
) -> pd.DataFrame:
    if not ruta_comparacion.exists():
        raise FileNotFoundError(
            f"No existe {ruta_comparacion}. Ejecuta primero scripts/comparar_sgp4_oem.py"
        )

    df = preparar_variables(pd.read_csv(ruta_comparacion))
    corte = int(len(df) * 0.75)

    # Primera prueba: entreno con el principio y compruebo si acierta el futuro.
    prueba_temporal = evaluar_modelo(
        df,
        df.index[:corte],
        df.index[corte:],
        "Validacion temporal: prediccion de tramo futuro",
    )

    # Segunda prueba: mezclo puntos para ver si aprende a calibrar ese mismo periodo.
    indices = np.arange(len(df))
    train_idx = df.index[indices % 4 != 0]
    test_idx = df.index[indices % 4 == 0]
    prueba_calibracion = evaluar_modelo(
        df,
        train_idx,
        test_idx,
        "Validacion intercalada: calibracion dentro de la ventana OEM",
    )

    modelo_final = RandomForestRegressor(n_estimators=300, random_state=42)
    modelo_final.fit(df[FEATURES], df[TARGETS])

    ruta_modelo.parent.mkdir(parents=True, exist_ok=True)
    ruta_resultados_temporal.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo_final, ruta_modelo)
    prueba_temporal.to_csv(ruta_resultados_temporal, index=False)
    prueba_calibracion.to_csv(ruta_resultados_calibracion, index=False)

    print(f"Modelo corrector guardado en: {ruta_modelo}")
    print(f"Resultados temporales guardados en: {ruta_resultados_temporal}")
    print(f"Resultados de calibracion guardados en: {ruta_resultados_calibracion}")
    return prueba_calibracion


if __name__ == "__main__":
    entrenar_corrector()
