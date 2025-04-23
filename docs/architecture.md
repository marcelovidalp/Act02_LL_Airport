# Sistema de Gestión de Aeropuerto - Documentación de Arquitectura

## Arquitectura del Sistema

El Sistema de Gestión de Aeropuerto sigue un patrón de arquitectura por capas y modular para asegurar la separación de responsabilidades, mantenibilidad y testabilidad.

### Capas

```mermaid
graph TD
    subgraph "Arquitectura por Capas"
        A[Cliente] --> B["Capa de Presentación<br>(FastAPI)"]
        B --> C["Capa de Servicio<br>(Lógica de Negocio)"]
        C --> D["Capa de Acceso a Datos<br>(SQLAlchemy)"]
        D --> E["Base de Datos<br>(SQLite)"]
    end
    
    style A fill:#f9f9f9,stroke:#333,stroke-width:1px
    style B fill:#d1e7dd,stroke:#0d6efd,stroke-width:2px
    style C fill:#fff3cd,stroke:#fd7e14,stroke-width:2px
    style D fill:#cfe2ff,stroke:#0d6efd,stroke-width:2px
    style E fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```

1. **Capa de Presentación**
   - Implementada usando FastAPI
   - Maneja peticiones y respuestas HTTP
   - Dirige llamadas API al servicio apropiado
   - Ubicada en `app/api/`

2. **Capa de Servicio**
   - Contiene la lógica de negocio
   - Actúa como intermediario entre API y acceso a datos
   - Implementa operaciones complejas sobre datos de vuelos
   - Ubicada en `app/services/`

3. **Capa de Acceso a Datos**
   - Maneja operaciones de base de datos usando SQLAlchemy
   - Define modelos de base de datos, esquemas y acceso a datos
   - Ubicada en `app/models/`, `app/schemas.py`, y `app/db.py`

4. **Capa de Infraestructura**
   - Configuración y gestión de conexiones a base de datos
   - Ubicada en `app/db.py`

### Estructura de Directorios Actual

```mermaid
graph TD
    Root["app/"] --> API["api/"]
    API --> init1["__init__.py"]
    API --> flight["flight_routes.py"]
    API --> list["list_routes.py"]
    
    Root --> Services["services/"]
    Services --> init2["__init__.py"]
    Services --> service["flight_service.py"]
    Services --> linked["linked_list.py"]
    
    Root --> Schemas["schemas/"]
    Schemas --> init3["__init__.py"]
    Schemas --> vuelo["vuelo_schemas.py"]
    Schemas --> lista["lista_schemas.py"]
    
    Root --> DB["db/"]
    DB --> init4["__init__.py"]
    DB --> config["config.py"]
    
    Root --> init5["__init__.py"]
    
    Root --> Models["models/"]
    Models --> Base["Base.py"]
    Models --> Estado["EstadoVuelo.py"]
    Models --> ListaM["ListaVuelos.py"]
    Models --> Nodo["Nodo.py"]
    Models --> Vuelo["Vuelo.py"]
    
    Docs["docs/"] --> api_doc["api_documentation.md"]
    Docs --> arq["architecture.md"]
    Docs --> visual["visual_guides.md"]
    Docs --> demo["demo_scenarios.md"]
```

## Flujo de Datos

```mermaid
sequenceDiagram
    participant Cliente as Cliente
    participant API as Capa API
    participant Servicio as Capa de Servicio
    participant Datos as Capa de Datos
    participant DB as Base de Datos
    
    Cliente->>API: 1. Petición HTTP
    API->>API: 2. Validación de datos
    API->>Servicio: 3. Llamada a función de servicio
    
    alt Operación de Lista
        Servicio->>Datos: 4a. Operación sobre lista enlazada
        Datos->>DB: 5a. Consulta/actualización DB
        DB-->>Datos: 6a. Resultados
        Datos-->>Servicio: 7a. Objetos procesados
    else Operación de Vuelo
        Servicio->>Datos: 4b. CRUD de vuelo
        Datos->>DB: 5b. Consulta/actualización DB
        DB-->>Datos: 6b. Resultados
        Datos-->>Servicio: 7b. Objetos procesados
    end
    
    Servicio-->>API: 8. Resultado de operación
    API-->>Cliente: 9. Respuesta HTTP formateada
```

## Componentes Clave

### Implementación de Lista Doblemente Enlazada

El sistema utiliza una lista doblemente enlazada para gestionar vuelos, con estos componentes clave:

```mermaid
classDiagram
    class Nodo {
        +vuelo: Vuelo
        +siguiente: Nodo
        +anterior: Nodo
    }
    
    class ListaVuelos {
        +nombre: String
        +cabeza: Nodo
        +cola: Nodo
        +añadirAlInicio(vuelo)
        +añadirAlFinal(vuelo)
        +eliminarDelInicio()
        +eliminarDelFinal()
        +insertarEnPosicion(vuelo, posicion)
        +eliminarDePosicion(posicion)
        +priorizar()
    }
    
    class Vuelo {
        +codigo: String
        +origen: String
        +destino: String
        +estado: EstadoVuelo
        +aerolinea: String
        +hora: DateTime
    }
    
    class EstadoVuelo {
        <<enumeration>>
        PROGRAMADO
        EMBARQUE
        DESPEGADO
        ATERRIZADO
        RETRASADO
        EMERGENCIA
        CANCELADO
    }
    
    ListaVuelos --> Nodo : contiene >
    Nodo --> Vuelo : contiene
    Nodo --> Nodo : anterior/siguiente
    Vuelo --> EstadoVuelo : estado
```

### Gestión de Vuelos

- Creación, recuperación y actualización de estado de vuelos
- Priorización de vuelos basada en estado (emergencias primero)
- Operaciones de lista como insertar, eliminar y reordenar vuelos

## Autenticación y Autorización

La implementación actual no incluye autenticación ni autorización. En un entorno de producción, se implementaría:

- Autenticación basada en JWT
- Control de acceso basado en roles
- Validación de claves de API

## Manejo de Errores

```mermaid
flowchart TD
    A[Petición Cliente] --> B{Validación de datos}
    B -->|Inválido| C[Error 400 Bad Request]
    B -->|Válido| D{Recurso existe?}
    D -->|No| E[Error 404 Not Found]
    D -->|Sí| F{Operación exitosa?}
    F -->|No| G[Error 500 Interno]
    F -->|Sí| H[Respuesta exitosa 200/201]
    
    C --> Z[Respuesta al Cliente]
    E --> Z
    G --> Z
    H --> Z
```

## Conclusión

Esta arquitectura proporciona una base sólida para el Sistema de Gestión de Aeropuerto, enfatizando:

- Modularidad y separación de responsabilidades
- Escalabilidad mediante diseño por capas
- Mantenibilidad con responsabilidades claras de los componentes
- Testabilidad con componentes aislados e interfaces bien definidas
