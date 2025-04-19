# Lista Doblemente Enlazada con Centinelas

## Descripción General
Una de las estructuras fundamentales del sistema es la lista doblemente enlazada con nodos centinela (header y trailer). Esta estructura permite gestionar eficientemente la secuencia de vuelos, facilitando la inserción, eliminación y reordenamiento según prioridades.

## Componentes Principales

### Clase Node
La clase `Node` representa cada elemento en la lista enlazada:

```python
class Node:
    def __init__(self, vuelo=None):
        self.vuelo = vuelo      # El vuelo almacenado
        self.next = None        # Referencia al siguiente nodo
        self.prev = None        # Referencia al nodo anterior
```

Características:
- **vuelo**: Referencia al objeto Vuelo asociado, o None si es un nodo centinela
- **next**: Puntero al siguiente nodo en la lista
- **prev**: Puntero al nodo anterior en la lista

Los nodos centinela siempre tienen `vuelo=None`, lo que los diferencia de los nodos regulares.

### Clase DoubleLinkedList
Esta clase implementa la lista doblemente enlazada usando centinelas:

```python
class DoubleLinkedList:
    def __init__(self):
        self.header = Node()    # Centinela de inicio
        self.trailer = Node()   # Centinela final
        
        # Conectar los centinelas
        self.header.next = self.trailer
        self.trailer.prev = self.header
        
        self._size = 0
```

La lista siempre tiene al menos dos nodos (los centinelas header y trailer), incluso cuando está vacía. Esto simplifica las operaciones de inserción y eliminación, evitando casos especiales para listas vacías.

## Operaciones Principales

### Inserción Entre Nodos
```python
def _insert_between(self, vuelo, predecessor, successor):
    """Inserta un nuevo nodo entre dos nodos existentes"""
    nuevo_nodo = Node(vuelo)
    nuevo_nodo.prev = predecessor
    nuevo_nodo.next = successor
    predecessor.next = nuevo_nodo
    successor.prev = nuevo_nodo
    self._size += 1
    return nuevo_nodo
```
Esta operación fundamental inserta un nuevo nodo entre dos nodos existentes, actualiza los punteros y aumenta el contador de tamaño.

### Inserción por Prioridad
```python
def insert_by_priority(self, vuelo):
    """
    Inserta un vuelo según su prioridad
    - Emergencia: al inicio
    - Regular: al final
    - Urgente: entre emergencias y regulares
    """
    if vuelo.prioridad == PrioridadVuelo.EMERGENCIA:
        return self.add_first(vuelo)
    # ...resto del código
```
Este método permite insertar vuelos según su nivel de prioridad, colocando emergencias al principio, vuelos regulares al final y vuelos urgentes en posiciones intermedias.

### Eliminación de Nodos
```python
def remove(self, node):
    """Elimina el nodo especificado de la lista"""
    if self.is_empty() or node is self.header or node is self.trailer:
        return None
    
    # Desconectar el nodo
    predecessor = node.prev
    successor = node.next
    predecessor.next = successor
    successor.prev = predecessor
    
    # Ayudar al garbage collector
    node.prev = node.next = None
    self._size -= 1
    
    return node.vuelo
```
Permite eliminar un nodo específico de la lista, reconectando los nodos adyacentes y liberando referencias para ayudar al recolector de basura.

### Reordenamiento por Prioridad
```python
def reorder_by_priority(self):
    """Reordena todos los vuelos según su prioridad actual"""
    if self._size <= 1:
        return  # Nada que reordenar
    
    # Crear una lista temporal con todos los vuelos
    vuelos = []
    current = self.header.next
    while current != self.trailer:
        vuelos.append(current.vuelo)
        current = current.next
    
    # Vaciar la lista original
    self.header.next = self.trailer
    self.trailer.prev = self.header
    self._size = 0
    
    # Volver a insertar los vuelos por prioridad
    for vuelo in vuelos:
        self.insert_by_priority(vuelo)
```
Este método permite reordenar toda la lista cuando cambian las prioridades de los vuelos, por ejemplo, cuando se declara una emergencia.

## Ventajas de la Implementación

### Uso de Centinelas
La utilización de nodos centinela (header y trailer) proporciona múltiples ventajas:

1. **Simplificación de algoritmos**: Elimina la necesidad de casos especiales para listas vacías o alteraciones en los extremos.
2. **Prevención de errores**: Reduce la posibilidad de errores de `NullPointerException` al garantizar que siempre haya nodos en los extremos.
3. **Operaciones más rápidas**: Simplifica la inserción y eliminación al principio y final de la lista.

### Eficiencia en Operaciones Críticas
- **Inserción al principio/final**: O(1) - Tiempo constante
- **Inserción en posición intermedia**: O(n) en el peor caso, pero típicamente más rápido para listas ordenadas
- **Eliminación de nodo conocido**: O(1) - Tiempo constante
- **Reordenamiento**: O(n log n) debido a la comparación de prioridades

## Aplicación en el Sistema
En nuestro sistema de aeropuerto, mantenemos dos listas doblemente enlazadas separadas:

1. **cola_despegues**: Gestiona la secuencia de vuelos para despegue
2. **cola_aterrizajes**: Gestiona la secuencia de vuelos para aterrizaje

Esta separación permite priorizar independientemente cada tipo de operación, potencialmente aplicando reglas diferentes según las necesidades operativas del aeropuerto.
