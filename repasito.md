# 📚 Estructuras de Datos - Resumen

## 🎯 Contenidos Principales

```mermaid
mindmap
  root((Estructuras))
    (TDA)
      (Pilas)
      (Colas)
      (Listas)
    (Árboles)
      (Heap)
      (BST)
    (Grafos)
      (Dirigidos)
      (No Dirigidos)
```

## 1. Tipos de Dato Abstracto (TDA)

### 1.1 Conceptos Básicos
- **Definición**: Modelo matemático con operaciones definidas
- **Implementación**: Independiente del lenguaje
- **Encapsulamiento**: Interfaz vs implementación

### 1.2 Ciclo de Vida TDA
```mermaid
graph LR
    A[Diseño] -->|Especificación| B[Implementación]
    B -->|Codificación| C[Uso]
    C -->|Mejoras| A
```

## 2. Estructuras Fundamentales

### 2.1 Pilas (LIFO)
```mermaid
graph TB
    A[Tope] --> B[Elemento 2]
    B --> C[Elemento 1]
    C --> D[Base]
```

**Operaciones**: O(1)
- push(elemento)
- pop()
- peek()
- isEmpty()

### 2.2 Colas (FIFO)
```mermaid
graph LR
    A[Frente] --> B[E1]
    B --> C[E2]
    C --> D[E3]
    D --> E[Final]
```

**Variantes**:
- Cola Simple
- Cola Circular
- Cola de Prioridad
- Deque

### 2.3 Listas Enlazadas
```mermaid
graph LR
    A[Head] --> B[Nodo 1]
    B --> C[Nodo 2]
    C --> D[Nodo 3]
    D --> E[Null]
```

**Tipos**:
- Simple
- Doble
- Circular

## 3. Árboles

### 3.1 Heap
```mermaid
graph TB
    A((10)) --> B((8))
    A --> C((9))
    B --> D((4))
    B --> E((5))
    C --> F((6))
    C --> G((7))
```

**Propiedades**:
- Completo o casi completo
- Max/Min Heap
- Operaciones O(log n)

### 3.2 Implementación Array
```python
class Heap:
    def __init__(self):
        self.heap = []
    
    def parent(self, i): return (i-1)//2
    def left(self, i): return 2*i + 1
    def right(self, i): return 2*i + 2
```

## 4. Complejidades
```mermaid
graph LR
    A[O(1)] --> B[O(log n)]
    B --> C[O(n)]
    C --> D[O(n log n)]
    D --> E[O(n²)]
```

## 5. Ejemplos Prácticos

### 5.1 Validador de Expresiones
```python
def validar_expresion(expr):
    pila = []
    pares = {')':'(', '}':'{', ']':'['}
    for c in expr:
        if c in '({[':
            pila.append(c)
        elif c in ')}]':
            if not pila or pila.pop() != pares[c]:
                return False
    return len(pila) == 0
```

### 5.2 Cola Circular
```mermaid
graph TD
    A[11] --> B[12]
    B --> C[15]
    C --> D[16]
    D --> E[17]
    E --> F[18]
    F --> G[9]
    G --> H[10]
    H --> A
```

## 🔍 Referencias Rápidas

| Estructura | Inserción | Eliminación | Búsqueda |
|------------|-----------|-------------|-----------|
| Pila | O(1) | O(1) | O(n) |
| Cola | O(1) | O(1) | O(n) |
| Lista | O(1) | O(1) | O(n) |
| Heap | O(log n) | O(log n) | O(1) |

## 📚 Recursos Adicionales
- [Visualizador de Estructuras](https://visualgo.net/)
- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)

## 📝 Preguntas para la Práctica

### TDA y Conceptos Básicos
1. Explica la diferencia entre la interfaz y la implementación de un TDA.
2. ¿Por qué es importante el encapsulamiento en los TDAs?
3. Diseña un TDA para representar una fracción matemática. Define sus operaciones básicas.

### Pilas
1. Implementa una función que determine si una cadena de paréntesis, corchetes y llaves está balanceada.
2. ¿Cómo implementarías una pila que también proporcione una operación para encontrar el mínimo elemento en tiempo O(1)?
3. Explica cómo se podría utilizar una pila para evaluar expresiones en notación polaca inversa (postfija).

### Colas
1. Implementa una cola usando dos pilas.
2. Diseña una estructura para simular el sistema de atención de un banco con clientes prioritarios.
3. ¿Qué ventajas ofrece una implementación circular de una cola frente a una implementación lineal?

### Listas Enlazadas
1. Escribe un algoritmo para detectar si una lista enlazada tiene un ciclo.
2. Implementa una función para invertir una lista enlazada in-place.
3. Diseña un algoritmo para encontrar el nodo medio de una lista enlazada en una sola pasada.

### Árboles
1. Explica cómo mantener las propiedades de un heap después de una inserción.
2. Implementa un algoritmo para imprimir los elementos de un BST en orden.
3. ¿Cuál es la diferencia principal entre una implementación de heap basada en array y una basada en nodos?

### Complejidad Algorítmica
1. Analiza la complejidad temporal y espacial de los siguientes algoritmos de ordenamiento: Bubble Sort, Merge Sort y Quick Sort.
2. ¿Cómo afecta el factor de carga a una tabla hash?
3. Proporciona un ejemplo de un algoritmo con complejidad O(n log n) y explica por qué tiene esta complejidad.

### Aplicaciones Prácticas
1. Diseña un sistema de gestión de tareas utilizando colas de prioridad.
2. Implementa un algoritmo para convertir una expresión infija a postfija usando una pila.
3. Utiliza una lista enlazada para implementar un sistema de reproducción de música con operaciones de avanzar, retroceder y repetir.

### Desafíos
1. Implementa un algoritmo eficiente para encontrar el camino más corto en un grafo ponderado.
2. Diseña una estructura de datos para un sistema de caché con política de reemplazo LRU (Least Recently Used).
3. Desarrolla un algoritmo para balancear un BST después de múltiples operaciones de inserción y eliminación.


