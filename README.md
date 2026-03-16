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
