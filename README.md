# tfg-sistema-localizacion-iss
Repositorio para el Trabajo de Fin de Grado: Sistema de localización de la Estación Espacial Internacional. Documentación, scripts, resultados y recursos.

### Objetivo del Proyecto: Optimización de Trayectoria de la ISS

Este diagrama visualiza cómo transformamos los datos brutos de la NASA en predicciones precisas utilizando Inteligencia Artificial, siguiendo un enfoque de ingeniería de sistemas alineado con ITIL.

```mermaid
graph LR
    %% Bloque 1: Entrada (Los Datos)
    A[ NASA / CelesTrak <br/>(Datos Brutos TLE) ]:::nasa

    %% Bloque 2: Tu Ingeniería (Procesos)
    subgraph "SISTEMA ISS-TRACKER-IA (Tu Aportación)"
        B( Motor Orbital SGP4 <br/>'Física Estándar' ):::proceso
        C{{ Dataset Histórico Validado <br/>(24h - 1440 puntos) }}:::datos
        D[ Modelo IA <br/>(Random Forest / XGBoost) ]:::ia
    end

    %% Bloque 3: Salida (El Valor)
    E(( Predicción de <br/>Trayectoria Precisa )):::valor

    %% Conexiones (El flujo de valor)
    A -->|Ingesta de Configuración| B
    B -->|Generación Ground Truth| C
    C -->|Entrenamiento y Test| D
    A -.->|Ajuste Dinámico BSTAR| D
    D -->|Inferencia de Trayectoria| E

    %% Estilos para que quede profesional en GitHub
    classDef nasa fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
    classDef proceso fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#333;
    classDef datos fill:#f5f5f5,stroke:#666666,stroke-width:2px,color:#333;
    classDef ia fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
    classDef valor fill:#d5e8d4,stroke:#82b366,stroke-width:4px,color:#333;
