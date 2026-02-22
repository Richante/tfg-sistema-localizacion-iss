# Funcionamiento del Sistema de Seguimiento Orbital (NASA/NORAD)

Para desarrollar un sistema de IA, es imperativo comprender el modelo matemático estándar que la NASA utiliza actualmente para localizar la ISS.

## 1. El Formato TLE (Two-Line Element Set)
La NASA distribuye la posición de la ISS mediante dos líneas de datos. Cada número tiene un significado físico concreto:

| Dato | Significado | Importancia para la IA |
| :--- | :--- | :--- |
| **Inclinación** | Ángulo de la órbita respecto al ecuador. | Define los límites de latitud norte/sur. |
| **Excentricidad** | Qué tan "circular" o "elíptica" es la órbita. | Indica variaciones en la velocidad. |
| **Movimiento Medio** | Cuántas vueltas da a la Tierra por día. | Es la base para predecir la posición futura. |
| **BSTAR (Drag)** | Coeficiente de resistencia atmosférica. | **Variable crítica** que la IA intentará optimizar. |

## 2. El Modelo de Propagación SGP4
La NASA no solo usa la posición actual, usa el algoritmo **SGP4** (Simplified General Perturbations). Este modelo calcula la posición futura considerando:
1. El achatamiento de la Tierra en los polos.
2. La resistencia del aire (que hace que la ISS pierda altura).
3. Las atracciones gravitatorias del Sol y la Luna.

## 3. Demostración de Validación
En el archivo `notebooks/01_obtencion_datos.ipynb`, hemos validado que al introducir un TLE oficial, el modelo SGP4 genera una trayectoria coherente con la realidad física observada en portales como *Spot the Station*.
