# Guías Visuales - Sistema de Gestión de Aeropuerto

## Lista Doblemente Enlazada: Visualización y Operaciones

### Estructura Básica

La lista doblemente enlazada es la estructura de datos fundamental que utilizamos para gestionar los vuelos. A continuación se muestra una representación visual de esta estructura:

```mermaid
graph LR
    ListaVuelos[("ListaVuelos")]
    N1["Nodo 1<br/>Vuelo: IB3456"]
    N2["Nodo 2<br/>Vuelo: FR1234"]
    N3["Nodo 3<br/>Vuelo: BA7890"]
    
    ListaVuelos -->|cabeza| N1
    ListaVuelos -->|cola| N3
    
    N1 -->|siguiente| N2
    N2 -->|siguiente| N3
    N3 -->|siguiente| null
    
    N1 -->|anterior| null
    N2 -->|anterior| N1
    N3 -->|anterior| N2
```

### Operaciones Básicas

#### 1. Añadir al Principio (add_first)

Añade un nuevo nodo al inicio de la lista.

```mermaid
graph LR
    subgraph "Antes"
        ListaA[("ListaVuelos")]
        A1["Nodo A"] -->|siguiente| A2["Nodo B"]
        A2 -->|siguiente| A3["Nodo C"]
        A2 -->|anterior| A1
        A3 -->|anterior| A2
        ListaA -->|cabeza| A1
        ListaA -->|cola| A3
    end
    
    subgraph "Después de add_first(Nodo X)"
        ListaB[("ListaVuelos")]
        B0["Nodo X"] -->|siguiente| B1["Nodo A"]
        B1 -->|siguiente| B2["Nodo B"]
        B2 -->|siguiente| B3["Nodo C"]
        B1 -->|anterior| B0
        B2 -->|anterior| B1
        B3 -->|anterior| B2
        ListaB -->|cabeza| B0
        ListaB -->|cola| B3
    end
```

#### 2. Añadir al Final (add_last)

Añade un nuevo nodo al final de la lista.

```mermaid
graph LR
    subgraph "Antes"
        ListaA[("ListaVuelos")]
        A1["Nodo A"] -->|siguiente| A2["Nodo B"]
        A2 -->|siguiente| A3["Nodo C"]
        A2 -->|anterior| A1
        A3 -->|anterior| A2
        ListaA -->|cabeza| A1
        ListaA -->|cola| A3
    end
    
    subgraph "Después de add_last(Nodo X)"
        ListaB[("ListaVuelos")]
        B1["Nodo A"] -->|siguiente| B2["Nodo B"]
        B2 -->|siguiente| B3["Nodo C"]
        B3 -->|siguiente| B4["Nodo X"]
        B2 -->|anterior| B1
        B3 -->|anterior| B2
        B4 -->|anterior| B3
        ListaB -->|cabeza| B1
        ListaB -->|cola| B4
    end
```

#### 3. Eliminar del Principio (remove_first)

Elimina el primer nodo de la lista.

```mermaid
graph LR
    subgraph "Antes"
        ListaA[("ListaVuelos")]
        A1["Nodo A"] -->|siguiente| A2["Nodo B"]
        A2 -->|siguiente| A3["Nodo C"]
        A2 -->|anterior| A1
        A3 -->|anterior| A2
        ListaA -->|cabeza| A1
        ListaA -->|cola| A3
    end
    
    subgraph "Después de remove_first()"
        ListaB[("ListaVuelos")]
        B2["Nodo B"] -->|siguiente| B3["Nodo C"]
        B3 -->|anterior| B2
        ListaB -->|cabeza| B2
        ListaB -->|cola| B3
    end
```

#### 4. Eliminar del Final (remove_last)

Elimina el último nodo de la lista.

```mermaid
graph LR
    subgraph "Antes"
        ListaA[("ListaVuelos")]
        A1["Nodo A"] -->|siguiente| A2["Nodo B"]
        A2 -->|siguiente| A3["Nodo C"]
        A2 -->|anterior| A1
        A3 -->|anterior| A2
        ListaA -->|cabeza| A1
        ListaA -->|cola| A3
    end
    
    subgraph "Después de remove_last()"
        ListaB[("ListaVuelos")]
        B1["Nodo A"] -->|siguiente| B2["Nodo B"]
        B2 -->|anterior| B1
        ListaB -->|cabeza| B1
        ListaB -->|cola| B2
    end
```

#### 5. Insertar en Posición (add_at_position)

Inserta un nodo en una posición específica.

```mermaid
graph LR
    subgraph "Antes"
        ListaA[("ListaVuelos")]
        A1["Nodo A"] -->|siguiente| A2["Nodo B"]
        A2 -->|siguiente| A3["Nodo C"]
        A2 -->|anterior| A1
        A3 -->|anterior| A2
        ListaA -->|cabeza| A1
        ListaA -->|cola| A3
    end
    
    subgraph "Después de add_at_position(Nodo X, 1)"
        ListaB[("ListaVuelos")]
        B1["Nodo A"] -->|siguiente| BX["Nodo X"]
        BX -->|siguiente| B2["Nodo B"]
        B2 -->|siguiente| B3["Nodo C"]
        BX -->|anterior| B1
        B2 -->|anterior| BX
        B3 -->|anterior| B2
        ListaB -->|cabeza| B1
        ListaB -->|cola| B3
    end
```

#### 6. Eliminar de Posición (remove_at_position)

Elimina un nodo de una posición específica.

```mermaid
graph LR
    subgraph "Antes"
        ListaA[("ListaVuelos")]
        A1["Nodo A"] -->|siguiente| A2["Nodo B"]
        A2 -->|siguiente| A3["Nodo C"]
        A2 -->|anterior| A1
        A3 -->|anterior| A2
        ListaA -->|cabeza| A1
        ListaA -->|cola| A3
    end
    
    subgraph "Después de remove_at_position(1)"
        ListaB[("ListaVuelos")]
        B1["Nodo A"] -->|siguiente| B3["Nodo C"]
        B3 -->|anterior| B1
        ListaB -->|cabeza| B1
        ListaB -->|cola| B3
    end
```

### Casos Especiales

#### Lista Vacía

```mermaid
graph LR
    ListaVacia[("ListaVuelos")]
    null1[NULL]
    null2[NULL]
    ListaVacia -->|cabeza| null1
    ListaVacia -->|cola| null2
```

#### Lista con Un Solo Elemento

```mermaid
graph LR
    Lista[("ListaVuelos")]
    Nodo["Nodo A"]
    Lista -->|cabeza| Nodo
    Lista -->|cola| Nodo
    Nodo -->|anterior| null
    Nodo -->|siguiente| null
```

### Priorización de Vuelos

La operación `prioritize_flights` reorganiza la lista según el estado de los vuelos:

```mermaid
graph LR
    subgraph "Antes"
        ListaA[("ListaVuelos")]
        A1["PROGRAMADO"] -->|siguiente| A2["EMERGENCIA"]
        A2 -->|siguiente| A3["EMBARQUE"]
        A3 -->|siguiente| A4["RETRASADO"]
        A2 -->|anterior| A1
        A3 -->|anterior| A2
        A4 -->|anterior| A3
        ListaA -->|cabeza| A1
        ListaA -->|cola| A4
    end
    
    subgraph "Después de prioritize_flights()"
        ListaB[("ListaVuelos")]
        B1["EMERGENCIA"] -->|siguiente| B2["EMBARQUE"]
        B2 -->|siguiente| B3["PROGRAMADO"]
        B3 -->|siguiente| B4["RETRASADO"]
        B2 -->|anterior| B1
        B3 -->|anterior| B2
        B4 -->|anterior| B3
        ListaB -->|cabeza| B1
        ListaB -->|cola| B4
    end
```

### Representación en Base de Datos

En nuestra implementación, la lista doblemente enlazada se representa mediante tres tablas principales:

```mermaid
erDiagram
    ListaVuelos ||--o{ Nodo : contiene
    Nodo ||--|| Vuelo : referencia
    Nodo ||--o{ Nodo : "anterior/siguiente"
    
    ListaVuelos {
        int id
        string nombre
        int cabeza_id
        int cola_id
    }
    
    Nodo {
        int id
        int vuelo_id
        int siguiente_id
        int anterior_id
    }
    
    Vuelo {
        int id
        string codigo
        string origen
        string destino
        datetime hora
        string aerolinea
        string puerta_embarque
        enum estado
    }
```

### Visualización de Estados de Vuelos

Cada vuelo tiene un estado que determina su prioridad en la lista:

```mermaid
graph TD
    subgraph "Prioridades de Estados"
        E1["EMERGENCIA (1)"] --> E2["EMBARQUE (2)"]
        E2 --> E3["PROGRAMADO (3)"]
        E3 --> E4["RETRASADO (4)"]
        E4 --> E5["DESPEGADO (5)"]
        E5 --> E6["ATERRIZADO (6)"]
        E6 --> E7["CANCELADO (7)"]
    end
```

### Flujo de Operaciones API

Este diagrama muestra cómo las operaciones API interactúan con la lista doblemente enlazada:

```mermaid
sequenceDiagram
    participant Cliente as Cliente (UI/Postman)
    participant API as API Endpoint
    participant Servicio as Servicio
    participant Lista as Lista Doblemente Enlazada
    
    Cliente->>API: Solicita operación
    API->>Servicio: Procesa solicitud
    Servicio->>Lista: Ejecuta operación en lista
    Lista-->>Servicio: Resultado de operación
    Servicio-->>API: Resultado procesado
    API-->>Cliente: Respuesta formateada
```

