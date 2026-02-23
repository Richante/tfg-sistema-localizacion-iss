/docs/sistema_localizacion_nasa.md

# Sistema Oficial de Localización de la ISS (NASA)

## Introducción:

La Estación Espacial Internacional (ISS) utiliza uno de los sistemas más avanzados de seguimiento orbital, desarrollado y gestionado por la NASA. Este sistema proporciona la posición, órbita y visibilidad de la ISS en tiempo real, siendo esencial para la navegación, comunicación y seguridad tanto de la estación como de las misiones asociadas. El objetivo de este documento es compilar los aspectos clave del sistema oficial, las herramientas y recursos públicos, y su importancia para estudios y simulaciones académicas.

## Herramienta oficial: Spot the Station:

La principal herramienta de consulta pública sobre la posición de la ISS es Spot the Station, disponible como web y app. Desarrollada por la NASA, ofrece:

Trayectorias en tiempo real, velocidad orbital, inclinación y posición de la ISS.

Calendarios (schedules) de visibilidad según región geográfica para observadores terrestres.

Datos descargables en formatos estándar como Orbit Ephemeris Message [.txt, .xml], conteniendo información como masa, área de drag, coeficiente de drag, maniobras agendadas y otros eventos orbitales relevantes.

Los datos orbitales y las previsiones son actualizados periódicamente por el equipo del Johnson Space Center en Houston (Trajectory Operations and Planning Officer).

https://www.nasa.gov/johnson/

## Funcionamiento del sistema y responsable

La localización y seguimiento se basa en:

Mediciones y cálculos precisos de la órbita, realizadas por el equipo especializado de planificación de trayectoria.

Actualizaciones frecuentes (unas 3 veces por semana) para corregir desviaciones por efectos atmosféricos.

Utilidad clave para:

Predecir pasos/sobrevuelo de la ISS en ciudades o regiones.

Mantener comunicaciones automáticas y programar acoplamientos con otras naves.

Realizar maniobras de seguridad y evasión de objetos.

Todos los datos generados son publicados en formatos abiertos para que puedan ser usados por investigadores, desarrolladores y educadores.

https://www.nasa.gov/spot-the-station/

## Visualización y APIs disponibles

La NASA y sus colaboradores ofrecen diversas plataformas y APIs para consultar y descargar datos:

NASA EarthData (APIs como GEDI Data API, CMR API): Permite acceso programático a datos históricos y actuales sobre la posición, física y eventos de la ISS.

https://www.earthdata.nasa.gov/

RadLab Visualization Portal: Visualizadores online de trayectoria y estado.

https://visualization.osdr.nasa.gov/

El código de la app “Spot the Station” se puede examinar y adaptar para simulaciones propias.

Desde ahí se accede a:

OSDR Biological Visualization Portal: visualiza datos biológicos de múltiples estudios.​

RadLab: visualiza datos de radiación (dosimetría) de distintas agencias espaciales.​

NBISC Biospecimen Search Tool: buscador de más de 100.000 muestras biológicas de vuelos espaciales y análogos en tierra.​

Biological Data API: API para acceder a datos biológicos complejos.​

Environmental Data Application (EDA): permite visualizar y comparar telemetría ambiental de la ISS (cabina, hardware) por misión.​

## Recursos complementarios (RadLab, Environmental Data App, HDEV)

RadLab Visualization Portal: Para acceso y descarga de telemetría y series temporales de instrumentos embarcados en la ISS.
https://visualization.osdr.nasa.gov/

Environmental Data App: Visualización de parámetros ambientales internos y externos de la estación según misiones.
https://visualization.osdr.nasa.gov/

HDEV Experimento NASA: Streaming de video en directo desde cámaras externas montadas en la ISS, útil para observaciones y validación de datos.

Tras el análisis de los recursos de la NASA, se identifica que el formato estándar para la interoperabilidad de datos orbitales es el TLE (Two-Line Element). Para la adquisición automatizada de estos datos en este proyecto, se utilizará el repositorio CelesTrak, que actúa como espejo oficial de los datos de seguimiento del NORAD/NASA.

https://eol.jsc.nasa.gov/

## Por qué investigar la web de la NASA

La NASA es la fuente oficial, precisa y más actualizada para datos espaciales, especialmente los relacionados con la ISS. Otras webs utilizan datos procedentes de NASA, por lo que investigar directamente aquí garantiza veracidad, actualidad y profundidad técnica. Es clave para la defensa del proyecto citar siempre fuentes de NASA, apps oficiales y sus APIs/datasets abiertos.


## Fuentes
nasa.gov

Spot the Station (NASA)

NASA EarthData

RadLab Visualization Portal

HDEV Experimento NASA

Johnson Space Center NASA

FAQ Spot the Station
