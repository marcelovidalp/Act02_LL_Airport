# Diagrama de Clases

## Visión General
El diagrama de clases muestra las principales entidades del sistema y sus relaciones. A continuación se presenta una vista simplificada del diseño orientado a objetos del sistema.

```
+-------------------+       +-------------------+       +-------------------+
| Vuelo             |       | Node              |       | DoubleLinkedList  |
+-------------------+       +-------------------+       +-------------------+
| id                |       | vuelo             |<----->| header            |
| numero_vuelo      |<------| next              |       | trailer           |
| aerolinea         |       | prev              |       | _size             |
| origen            |       +-------------------+       +-------------------+
| destino           |               ^                   | add_first()       |
| hora_programada   |               |                   | add_last()        |
| tipo_vuelo        |               |                   | insert_by_priority()|
| prioridad         |       +-------------------+       | remove()          |
| tipo_emergencia   |       | Centinel          |       | reorder_by_priority()|
| estado            |       | (Node sin vuelo)  |       +-------------------+
| demora_minutos    |       +-------------------+               ^
+-------------------+                                           |
        ^                                                       |
        |                                              +-------------------+
        |                                              | VueloService      |
+-------------------+                                  +-------------------+
| BaseRepository<T> |                                  | repository        |
+-------------------+                                  | cola_despegues    |
| get_by_id()       |                                  | cola_aterrizajes  |
| get_all()         |                                  +-------------------+
| add()             |                                  | agregar_vuelo()   |
| update()          |                                  | declarar_emergencia()|
| delete()          |                                  | aplicar_demora()  |
+-------------------+                                  | obtener_proximo_vuelo()|
        ^                                              +-------------------+
        |                                                       ^
        |                                                       |
+-------------------+                                  +-------------------+
| VueloRepository   |                                  | FastAPI Routes    |
+-------------------+                                  +-------------------+
| session           |<---------------------------------| service           |
+-------------------+                                  +-------------------+
| get_by_id()       |                                  | crear_vuelo()     |
| get_all()         |                                  | declarar_emergencia()|
| add()             |                                  | aplicar_demora()  |
| update()          |                                  | obtener_proximo_vuelo()|
| delete()          |                                  +-------------------+
| get_by_numero_vuelo()|
| get_vuelos_por_estado()|
+-------------------+
```

## Relaciones Principales

### 1. DoubleLinkedList y Node
- La lista doblemente enlazada (`DoubleLinkedList`) contiene referencias a nodos centinela (`header` y `trailer`).
- Cada `Node` puede contener una referencia a un `Vuelo` y tiene enlaces a los nodos anterior (`prev`) y siguiente (`next`).
- Los nodos centinela son instancias de `Node` pero con `vuelo=None`.

### 2. VueloService y DoubleLinkedList
- `VueloService` mantiene dos instancias de `DoubleLinkedList`: `cola_despegues` y `cola_aterrizajes`.
- Utiliza estas listas para gestionar la secuencia de vuelos según su tipo.

### 3. VueloService y VueloRepository
- `VueloService` utiliza `VueloRepository` para operaciones de persistencia.
- Aplica lógica de negocio antes/después de las operaciones de base de datos.

### 4. FastAPI Routes y VueloService
- Los endpoints de API utilizan `VueloService` para ejecutar operaciones de negocio.
- Transforman los DTOs (Pydantic models) en entidades del dominio.

### 5. VueloRepository y BaseRepository
- `VueloRepository` implementa la interfaz `BaseRepository<Vuelo>`.
- Proporciona operaciones específicas para la entidad `Vuelo`.

## Patrones de Diseño Aplicados

### Patrón Repository
Representado por la jerarquía `BaseRepository` -> `VueloRepository`, que abstrae el acceso a datos.

### Inyección de Dependencias
Las dependencias (como `VueloRepository`) se inyectan en las clases que las utilizan (`VueloService`), facilitando la prueba y el mantenimiento.

### Patrón Estrategia (implícito)
La lógica de priorización en `DoubleLinkedList.insert_by_priority()` implementa diferentes estrategias según el tipo de vuelo.

## Principios SOLID

### Principio de Responsabilidad Única (SRP)
Cada clase tiene una única responsabilidad bien definida:
- `Vuelo`: Representar datos de un vuelo
- `Node`: Elemento en una lista enlazada
- `DoubleLinkedList`: Gestionar secuencias de nodos
- `VueloRepository`: Operaciones de persistencia
- `VueloService`: Lógica de negocio

### Principio Abierto/Cerrado (OCP)
El sistema está diseñado para ser extendido sin modificar componentes existentes, por ejemplo, agregando nuevas estrategias de priorización.

### Principio de Sustitución de Liskov (LSP)
Las implementaciones de repositorio respetan la interfaz `BaseRepository` y pueden ser sustituidas sin afectar al sistema.

### Principio de Segregación de Interfaces (ISP)
Las interfaces están diseñadas específicamente para sus clientes, evitando dependencias innecesarias.

### Principio de Inversión de Dependencias (DIP)
Las dependencias fluyen hacia abstracciones, no hacia implementaciones concretas, como se ve en la relación entre `VueloService` y `BaseRepository`.
