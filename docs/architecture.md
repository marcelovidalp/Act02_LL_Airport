# Sistema de Gestión de Aeropuerto - Documentación de Arquitectura

## Arquitectura del Sistema

El Sistema de Gestión de Aeropuerto sigue una arquitectura por capas y modular para asegurar la separación de responsabilidades, mantenibilidad y testabilidad. La implementación utiliza una estructura de datos de lista doblemente enlazada en memoria para gestionar los vuelos, con persistencia en la base de datos.

### Capas

```mermaid
graph TD
    subgraph "Arquitectura por Capas"
        A[Cliente] --> B["Capa de Presentación<br>(FastAPI)"]
        B --> C["Capa de Aplicación<br>(Servicios)"]
        C --> D1["Capa de Dominio<br>(Lógica de Negocio)"]
        C --> D2["Capa de Repositorio<br>(Acceso a Datos)"]
        D2 --> E["Base de Datos<br>(SQLite)"]
    end
    
    style A fill:#f9f9f9,stroke:#333,stroke-width:1px
    style B fill:#d1e7dd,stroke:#0d6efd,stroke-width:2px
    style C fill:#fff3cd,stroke:#fd7e14,stroke-width:2px
    style D1 fill:#e2f0fb,stroke:#0d6efd,stroke-width:2px
    style D2 fill:#cfe2ff,stroke:#0d6efd,stroke-width:2px
    style E fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```

1. **Capa de Presentación (API)**
   - Implementada usando FastAPI
   - Maneja peticiones y respuestas HTTP
   - Dirige llamadas API al servicio apropiado
   - Ubicada en `app/api/`

2. **Capa de Aplicación (Servicios)**
   - Contiene la lógica de aplicación
   - Coordina entre API, dominio y repositorios
   - Implementa operaciones complejas sobre datos de vuelos
   - Ubicada en `app/services/`

3. **Capa de Dominio**
   - Implementa la lógica de negocio
   - Contiene la implementación de la lista doblemente enlazada en memoria
   - Ubicada en `app/domain/`

4. **Capa de Repositorio**
   - Maneja operaciones de base de datos usando SQLAlchemy
   - Abstrae el acceso a datos para la capa de servicio
   - Ubicada en `app/repositories/`

5. **Capa de Base de Datos**
   - Configuración y gestión de conexiones a base de datos
   - Ubicada en `app/db/`

### Estructura del Proyecto Refactorizada

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
    Services --> manager["linked_list_manager.py"]
    
    Root --> Domain["domain/"]
    Domain --> init_domain["__init__.py"]
    Domain --> memory_list["memory_linked_list.py"]
    Domain --> memory_node["in_memory_node.py"]
    
    Root --> Repos["repositories/"]
    Repos --> init_repo["__init__.py"]
    Repos --> flight_repo["flight_repository.py"]
    
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
    Models --> Vuelo["Vuelo.py"]
    
    Docs["docs/"] --> api_doc["api_documentation.md"]
    Docs --> arq["architecture.md"]
    Docs --> visual["visual_guides.md"]
    Docs --> demo["demo_scenarios.md"]
```

## Patrón de Lista Doblemente Enlazada en Memoria

Una de las principales características de esta arquitectura es la implementación de la lista doblemente enlazada **exclusivamente en memoria**. Esto ofrece varias ventajas:

1. **Mayor Eficiencia**: Las operaciones en memoria son significativamente más rápidas que las operaciones de base de datos
2. **Implementación más Limpia**: Al separar la estructura de datos de la persistencia, se logra un código más modular
3. **Flexibilidad**: Es más fácil modificar la implementación de la lista sin afectar la persistencia

El sistema utiliza un **caché en memoria** para almacenar las listas enlazadas, que se construyen a partir de los datos de la base de datos cuando son requeridas. Esto proporciona una combinación óptima de rendimiento y persistencia.

```mermaid
sequenceDiagram
    participant Cliente as Cliente
    participant API as API Endpoint
    participant Servicio as Servicio
    participant ListaManager as LinkedListManager
    participant Repositorio as Repository
    participant DB as Base de Datos
    
    Cliente->>API: Solicita operación
    API->>Servicio: Procesa solicitud
    
    alt Primera solicitud a la lista
        Servicio->>ListaManager: Obtener lista
        ListaManager->>Repositorio: Cargar vuelos
        Repositorio->>DB: Consultar vuelos
        DB-->>Repositorio: Datos de vuelos
        Repositorio-->>ListaManager: Vuelos
        ListaManager->>ListaManager: Construir lista en memoria
    else Lista ya en caché
        Servicio->>ListaManager: Obtener lista (desde caché)
    end
    
    Servicio->>ListaManager: Ejecutar operación
    ListaManager->>Repositorio: Actualizar en la BD si es necesario
    Repositorio->>DB: Guardar cambios
    DB-->>Repositorio: Confirmar cambios
    
    ListaManager-->>Servicio: Resultado
    Servicio-->>API: Resultado procesado
    API-->>Cliente: Respuesta HTTP
```

## Modelo de Datos Simplificado

En la versión refactorizada del sistema, el modelo de datos se ha simplificado eliminando la tabla de nodos de la base de datos:

```mermaid
classDiagram
    class Vuelo {
        +id: int
        +codigo: string
        +origen: string
        +destino: string
        +hora: datetime
        +aerolinea: string
        +puerta_embarque: string
        +estado: EstadoVuelo
        +lista_vuelos_id: int
    }
    
    class ListaVuelos {
        +id: int
        +nombre: string
    }
    
    ListaVuelos "1" --> "*" Vuelo: contiene
```

Esto se complementa con la estructura en memoria:

```mermaid
classDiagram
    class Node~T~ {
        +data: T
        +next: Node<T>
        +prev: Node<T>
    }
    
    class MemoryLinkedList~T~ {
        -head: Node<T>
        -tail: Node<T>
        -size: int
        +add_first(data: T)
        +add_last(data: T)
        +insert_at(pos: int, data: T)
        +remove_first(): T
        +remove_last(): T
        +remove_at(pos: int): T
        +get_first(): T
        +get_last(): T
        +get_all(): List<T>
    }
    
    class LinkedListManager {
        -_lists_cache: Dict[int, MemoryLinkedList]
        +get_list_instance(db, lista_id)
        +add_first(db, lista_id, vuelo)
        +add_last(db, lista_id, vuelo)
        +prioritize(db, lista_id)
    }
    
    MemoryLinkedList --> Node : usa
    LinkedListManager --> MemoryLinkedList : gestiona
```

## Patrones de Diseño Implementados

### 1. Repository Pattern

Separa la lógica de acceso a datos de la lógica de negocio. Los repositorios (`FlightRepository` y `ListRepository`) abstraen las operaciones de base de datos.

### 2. Service Layer Pattern

Implementa la lógica de aplicación en servicios que coordinan entre capas (`FlightService` y `LinkedListManager`).

### 3. Adapter Pattern

El módulo `linked_list.py` actúa como un adaptador entre la API existente y la nueva implementación `LinkedListManager`.

### 4. Cache Pattern

`LinkedListManager` implementa un sistema de caché para las listas enlazadas en memoria.

### 5. Factory Method

Se utiliza en `LinkedListManager` para crear instancias de listas enlazadas según sea necesario.

## Flujo de Datos y Operaciones

```mermaid
flowchart TD
    A[Request HTTP] --> B{Endpoint de Vuelos}
    B -->|Crear Vuelo| C[FlightService]
    B -->|Gestionar Lista| D[LinkedListManager]
    
    C -->|Persistencia| E[FlightRepository]
    D -->|Operaciones en Memoria| F[MemoryLinkedList]
    
    E -->|SQL| G[Base de Datos]
    F -->|Recupera/Guarda| E
    
    C -->|Retorna| H[Respuesta HTTP]
    D -->|Retorna| H
```

## Sincronización y Consistencia

Para mantener la consistencia entre la estructura en memoria y los datos persistentes:

1. Cada operación que modifica la estructura de la lista también actualiza las relaciones en la base de datos
2. Cuando se modifica un estado de vuelo, se puede forzar una reconstrucción de la lista en memoria
3. La caché de listas se puede limpiar para forzar la recarga desde la base de datos

Este enfoque garantiza que las operaciones sean eficientes mientras se mantiene la persistencia de datos.

## Conclusión

La arquitectura refactorizada separa claramente las responsabilidades:

- **Datos Persistentes**: Vuelos y sus atributos, listas de vuelos
- **Estructura en Memoria**: Nodos y estructura de lista doblemente enlazada
- **Lógica de Negocio**: Reglas de priorización y gestión de vuelos

Esto resulta en un sistema más mantenible, con mejor rendimiento y mayor flexibilidad para cambios futuros.
