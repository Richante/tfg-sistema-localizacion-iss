# Validacion SGP4 vs IA con datos NASA OEM

## Idea

La primera version del proyecto generaba una trayectoria de la ISS usando TLE
y SGP4. Eso sirve para tener una base orbital, pero no demuestra por si solo
que la IA mejore a SGP4.

Para hacer una comparacion mas seria se anade una segunda fase:

1. Se descarga el TLE actual de la ISS desde CelesTrak.
2. Se descarga la efemeride OEM oficial de NASA Spot the Station.
3. Se calcula con SGP4 la posicion de la ISS en los mismos instantes del OEM.
4. Se mide el error entre `NASA OEM` y `SGP4`.
5. La IA aprende el residuo:

```text
residuo = posicion_oem_nasa - posicion_sgp4
```

La prediccion final queda asi:

```text
posicion_corregida = posicion_sgp4 + residuo_predicho_por_ia
```

## Por que tiene sentido

SGP4 es el modelo base recomendado para trabajar con TLE, pero la ISS esta en
orbita baja y su trayectoria se ve afectada por rozamiento atmosferico,
actividad solar, maniobras y cambios operacionales. NASA explica en Spot the
Station que la atmosfera fina puede hacer que la trayectoria proyectada acumule
pequenos errores, y que por eso sus controladores actualizan los datos varias
veces por semana.

La IA no sustituye a SGP4. En este proyecto se usa como una capa correctora
encima de SGP4.

## Scripts anadidos

```text
scripts/descargar_tle_celestrak.py
scripts/descargar_oem_nasa.py
scripts/comparar_sgp4_oem.py
scripts/entrenar_corrector_ia.py
scripts/ejecutar_validacion_oem.py
```

## Ejecucion

Desde la raiz del repositorio:

```bash
python scripts/ejecutar_validacion_oem.py
```

Tambien se puede ejecutar paso a paso:

```bash
python scripts/descargar_tle_celestrak.py
python scripts/descargar_oem_nasa.py
python scripts/comparar_sgp4_oem.py
python scripts/entrenar_corrector_ia.py
```

## Resultado esperado

El script genera:

```text
data/iss_tle_actual.txt
data/ISS.OEM_J2K_EPH.txt
data/comparacion_sgp4_oem.csv
models/modelo_corrector_sgp4_oem.joblib
results/evaluacion_corrector_ia_temporal.csv
results/evaluacion_corrector_ia_calibracion.csv
```

Estos archivos se consideran resultados generados y no se suben al repositorio
por defecto. Se pueden volver a crear ejecutando el flujo principal.

La defensa se basa en comparar:

```text
Error SGP4 vs NASA OEM
Error SGP4 + IA vs NASA OEM
```

El script muestra dos modos:

```text
Validacion temporal
```

Entrena con el primer 75% de la ventana OEM y prueba con el tramo futuro. Es la
prueba mas exigente porque evalua capacidad de prediccion futura.

```text
Validacion intercalada
```

Entrena con puntos repartidos por toda la ventana OEM y prueba con puntos no
vistos intercalados. Esta prueba mide si la IA puede actuar como calibrador del
error SGP4 dentro de una ventana orbital conocida.

Si la IA mejora en el modo intercalado, se puede defender que el sistema aprende
una correccion util cuando dispone de datos oficiales recientes. Si no mejora en
el modo temporal, el resultado tambien es util: demuestra que SGP4 ya es una
base muy fuerte y que para predecir mejor el futuro hacen falta mas datos
historicos o variables externas.

## Fuentes

- NASA Spot the Station: https://www.nasa.gov/spot-the-station/
- ISS Trajectory Data: https://spotthestation.nasa.gov/trajectory_data.cfm
- CelesTrak GP/TLE: https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle
