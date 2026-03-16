# tfg-sistema-localizacion-iss
Repositorio para el Trabajo de Fin de Grado: Sistema de localización de la Estación Espacial Internacional. Documentación, scripts, resultados y recursos.

### Objetivo del Proyecto: Optimización de Trayectoria de la ISS

```mermaid
graph LR
    %% Bloque 1: Entrada
    A[NASA - Datos Brutos TLE]:::nasa

    %% Bloque 2: Tu Ingeniería
    subgraph SISTEMA_ISS_TRACKER_IA
        B(Motor Orbital SGP4):::proceso
        C[(Dataset Historico 24h)]:::datos
        D[Modelo IA - Random Forest]:::ia
    end

    %% Bloque 3: Salida
    E((Prediccion Precisa)):::valor

    %% Conexiones
    A --> B
    B --> C
    C --> D
    D --> E

    %% Estilos simples
    classDef nasa fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
    classDef proceso fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
    classDef datos fill:#f5f5f5,stroke:#666666,stroke-width:2px;
    classDef ia fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
    classDef valor fill:#d5e8d4,stroke:#82b366,stroke-width:4px;




### Objetivo Principal: Comparación de Modelos de Predicción

El objetivo de este proyecto de ingeniería es realizar un **benchmarking** (estudio comparativo) para evaluar la precisión de dos enfoques distintos en la predicción de la trayectoria de la ISS. Buscamos demostrar que un modelo de Inteligencia Artificial puede superar la precisión del modelo físico estándar cuando se ajusta dinámicamente.

```mermaid
graph TD
    %% Entrada Común (Nivel 1)
    A[ NASA - Datos Brutos TLE ]:::nasa

    %% Los Dos Caminos (Nivel 2)
    subgraph CAMINO_1__FISICA_ESTANDAR
        B( Motor Orbital SGP4 ):::proceso
        C[( Resultado 1: Trayectoria Teorica )]:::datos
    end

    subgraph CAMINO_2__IA_AVANZADA
        D[ Modelo IA - Random Forest / XGBoost ]:::ia
        E[( Resultado 2: Trayectoria Mejorada )]:::datos
    end

    %% El Objetivo Final: La Comparación (Nivel 3)
    F{{ OBJETIVO FINAL: ANALISIS DE RESIDUOS Y COMPARATIVA }}:::valor

    %% Conexiones (Flujo)
    A --> B
    B --> C
    A --> D
    D --> E
    
    C --> F
    E --> F

    %% Estilos Profesionales
    classDef nasa fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
    classDef proceso fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#333;
    classDef datos fill:#f5f5f5,stroke:#666666,stroke-width:2px,color:#333;
    classDef ia fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
    classDef valor fill:#d5e8d4,stroke:#82b366,stroke-width:4px,color:#333;

