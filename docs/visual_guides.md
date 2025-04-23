# Guías Visuales - Sistema de Gestión de Aeropuerto

## Lista Doblemente Enlazada: Visualización y Operaciones

### Estructura Básica

La lista doblemente enlazada es la estructura de datos fundamental que utilizamos para gestionar los vuelos. A continuación se muestra una representación visual de esta estructura:

```
    +----------------+      +----------------+      +----------------+
    |    Nodo 1      |      |    Nodo 2      |      |    Nodo 3      |
    |                |      |                |      |                |
    | Vuelo: IB3456  |      | Vuelo: FR1234  |      | Vuelo: BA7890  |
    | anterior: NULL +<-----+ anterior       +<-----+ anterior       |
    | siguiente      +----->+ siguiente      +----->+ siguiente: NULL|
    +----------------+      +----------------+      +----------------+
            ^                                              ^
            |                                              |
+----------------------+                                   |
|   ListaVuelos        |                                   |
|                      |                                   |
|   cabeza             +-----------------------------------+
|   cola               +-----------------------------------+
+----------------------+
```

### Operaciones Básicas

#### 1. Añadir al Principio (add_first)

Añade un nuevo nodo al inicio de la lista.

```
Antes:
cabeza -> [Nodo A] <-> [Nodo B] <-> [Nodo C] <- cola

Después de add_first([Nodo X]):
cabeza -> [Nodo X] <-> [Nodo A] <-> [Nodo B] <-> [Nodo C] <- cola
```

#### 2. Añadir al Final (add_last)

Añade un nuevo nodo al final de la lista.

```
Antes:
cabeza -> [Nodo A] <-> [Nodo B] <-> [Nodo C] <- cola

Después de add_last([Nodo X]):
cabeza -> [Nodo A] <-> [Nodo B] <-> [Nodo C] <-> [Nodo X] <- cola
```

#### 3. Eliminar del Principio (remove_first)

Elimina el primer nodo de la lista.

```
Antes:
cabeza -> [Nodo A] <-> [Nodo B] <-> [Nodo C] <- cola

Después de remove_first():
cabeza -> [Nodo B] <-> [Nodo C] <- cola
```

#### 4. Eliminar del Final (remove_last)

Elimina el último nodo de la lista.

```
Antes:
cabeza -> [Nodo A] <-> [Nodo B] <-> [Nodo C] <- cola

Después de remove_last():
cabeza -> [Nodo A] <-> [Nodo B] <- cola
```

#### 5. Insertar en Posición (add_at_position)

Inserta un nodo en una posición específica.

```
Antes:
cabeza -> [Nodo A] <-> [Nodo B] <-> [Nodo C] <- cola

Después de add_at_position([Nodo X], 1):
cabeza -> [Nodo A] <-> [Nodo X] <-> [Nodo B] <-> [Nodo C] <- cola
```

#### 6. Eliminar de Posición (remove_at_position)

Elimina un nodo de una posición específica.

```
Antes:
cabeza -> [Nodo A] <-> [Nodo B] <-> [Nodo C] <- cola

Después de remove_at_position(1):
cabeza -> [Nodo A] <-> [Nodo C] <- cola
```

### Casos Especiales

#### Lista Vacía

```
cabeza -> NULL
cola -> NULL
```

#### Lista con Un Solo Elemento

```
cabeza -> [Nodo A] <- cola
```

### Priorización de Vuelos

La operación `prioritize_flights` reorganiza la lista según el estado de los vuelos:

1. Primero: Vuelos en EMERGENCIA
2. Segundo: Vuelos en EMBARQUE
3. Tercero: Vuelos PROGRAMADOS
4. Resto: Otros estados

```
Antes:
cabeza -> [PROGRAMADO] <-> [EMERGENCIA] <-> [EMBARQUE] <-> [RETRASADO] <- cola

Después de prioritize_flights():
cabeza -> [EMERGENCIA] <-> [EMBARQUE] <-> [PROGRAMADO] <-> [RETRASADO] <- cola
```

### Representación en Base de Datos

En nuestra implementación, la lista doblemente enlazada se representa mediante tres tablas principales:

1. **ListaVuelos**: Contiene referencias a los nodos cabeza y cola
2. **Nodo**: Contiene referencias al vuelo y a los nodos anterior y siguiente
3. **Vuelo**: Contiene los datos del vuelo

```
+-------------+       +-------+       +--------+
| ListaVuelos |------>| Nodo  |------>| Vuelo  |
+-------------+       +-------+       +--------+
                         |
                         v
                      +-------+       +--------+
                      | Nodo  |------>| Vuelo  |
                      +-------+       +--------+
                         |
                         v
                      +-------+       +--------+
                      | Nodo  |------>| Vuelo  |
                      +-------+       +--------+
```

### Visualización de Estados de Vuelos

Cada vuelo tiene un estado que determina su prioridad en la lista:

```
+----------------+----------------+----------------+
|  EMERGENCIA    |   EMBARQUE     |  PROGRAMADO    |
| (Prioridad 1)  | (Prioridad 2)  | (Prioridad 3)  |
+----------------+----------------+----------------+
|   RETRASADO    |   DESPEGADO    |   ATERRIZADO   |
| (Prioridad 4)  | (Prioridad 5)  | (Prioridad 6)  |
+----------------+----------------+----------------+
|   CANCELADO    |
| (Prioridad 7)  |
+----------------+
```

### Flujo de Operaciones API

Este diagrama muestra cómo las operaciones API interactúan con la lista doblemente enlazada:

```
   Cliente       ->   API Endpoint   ->   Servicio      ->   Lista Doblemente
   (Postman/UI)      (flight_routes)     (flight_service)       Enlazada
       |                   |                  |                     |
       | Solicita          |                  |                     |
       | operación         |                  |                     |
       v                   v                  |                     |
       +------------------->                  |                     |
       |                   | Procesa solicitud|                     |
       |                   v                  |                     |
       |                   +----------------->                     |
       |                   |                  | Ejecuta operación   |
       |                   |                  | en lista            |
       |                   |                  v                     |
       |                   |                  +-------------------->
       |                   |                  |                     | Modifica
       |                   |                  |                     | estructura
       |                   |                  |                     v
       |                   |                  |<--------------------+
       |                   |<-----------------+                     |
       |<------------------+                  |                     |
       | Recibe respuesta  |                  |                     |
       v                   |                  |                     |

