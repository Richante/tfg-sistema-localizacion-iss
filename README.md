# tfg-sistema-localizacion-iss
Repositorio para el Trabajo de Fin de Grado: Sistema de localización de la Estación Espacial Internacional. Documentación, scripts, resultados y recursos.

### Objetivo del TFG: Corrección del Error Predictivo Orbital (NASA vs IA)

```mermaid
graph TD
    A[ NASA - Datos Brutos TLE ]:::nasa

    subgraph MODELO_TRADICIONAL
        B( Algoritmo SGP4 ):::proceso
        C[( Prediccion Teorica NASA )]:::datos
    end

    subgraph MI_SISTEMA_INTELIGENTE
        D[ Red Neuronal / IA ]:::ia
        E[( Prediccion Corregida por IA )]:::datos
    end

    F{ ¿Cual se acerca mas a la realidad? }:::valor

    A --> B
    B --> C
    
    A --> D
    C -.->|Se usa como base| D
    D --> E

    C --> F
    E --> F

    classDef nasa fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
    classDef proceso fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
    classDef datos fill:#f5f5f5,stroke:#666666,stroke-width:2px;
    classDef ia fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
    classDef valor fill:#d5e8d4,stroke:#82b366,stroke-width:4px;
```

## Validacion SGP4 vs IA

La fase nueva del proyecto compara una prediccion SGP4 basada en TLE contra la
efemeride OEM oficial de NASA Spot the Station. La IA se usa como corrector del
residuo entre ambas trayectorias.

Flujo principal:

```bash
python scripts/ejecutar_validacion_oem.py
```

Documentacion: `docs/validacion_sgp4_vs_ia.md`
