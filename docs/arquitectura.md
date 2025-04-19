# Arquitectura del Sistema

## Visión General
El sistema de gestión de aeropuerto implementa una arquitectura por capas que separa claramente las responsabilidades y mejora la mantenibilidad. Esta arquitectura facilita la aplicación de los principios SOLID.

## Estructura de Directorios
```
Act02_LL_Airport/
├── models/                # Modelos de datos (ORM)
├── domain/                # Entidades y lógica core (lista enlazada)
├── repositories/          # Patrón Repository para acceso a datos
├── services/              # Servicios de negocio
├── api/                   # FastAPI endpoints
├── config/                # Configuración
└── main.py                # Punto de entrada
```

## Descripción de Capas

### 1. Capa de Modelos
La capa de modelos define las entidades persistentes utilizando SQLAlchemy ORM.

**Responsabilidades:**
- Definir la estructura de datos
- Mapear objetos a tablas de la base de datos
- Proporcionar métodos básicos de las entidades

**Archivos principales:**
- `/models/vuelo.py`: Define la entidad Vuelo y enumeraciones relacionadas

### 2. Capa de Dominio
La capa de dominio contiene la lógica central del negocio, incluyendo la implementación de la lista doblemente enlazada.

**Responsabilidades:**
- Implementar estructuras de datos especializadas
- Proporcionar la lógica de negocio core

**Archivos principales:**
- `/domain/linked_list/node.py`: Implementación de nodos
- `/domain/linked_list/double_linked_list.py`: Lista doblemente enlazada con centinelas

### 3. Capa de Repositorios
Implementa el patrón Repository para abstraer el acceso a datos.

**Responsabilidades:**
- Proporcionar una abstracción sobre el acceso a datos
- Encapsular la lógica de consultas y persistencia
- Facilitar las pruebas unitarias mediante la separación de la lógica de acceso a datos

**Archivos principales:**
- `/repositories/base_repository.py`: Interfaz base para todos los repositorios
- `/repositories/vuelo_repository.py`: Implementación específica para vuelos

### 4. Capa de Servicios
Coordina operaciones entre repositorios y aplica lógica de negocio compleja.

**Responsabilidades:**
- Coordinar operaciones entre diferentes repositorios
- Implementar lógica de negocio compleja
- Aplicar reglas de validación

**Archivos principales:**
- `/services/vuelo_service.py`: Servicio para gestión de vuelos

### 5. Capa de API
Expone la funcionalidad del sistema a través de una API RESTful.

**Responsabilidades:**
- Definir endpoints REST
- Validar entrada de usuarios
- Transformar DTOs a entidades y viceversa

**Archivos principales:**
- `/api/schemas/vuelo_schema.py`: Esquemas Pydantic para serialización/deserialización
- `/api/routes/vuelo_routes.py`: Definición de endpoints FastAPI

## Aplicación de Principios SOLID

### Principio de Responsabilidad Única (SRP)
Cada clase tiene una única responsabilidad. Por ejemplo, `VueloRepository` solo maneja el acceso a datos de vuelos, mientras que `VueloService` maneja la lógica de negocio.

### Principio Abierto/Cerrado (OCP)
El sistema está diseñado para ser extensible sin modificar código existente. Por ejemplo, podemos agregar nuevas estrategias de priorización sin cambiar la clase `DoubleLinkedList`.

### Principio de Sustitución de Liskov (LSP)
Las implementaciones de repositorios pueden ser sustituidas siempre que cumplan con la interfaz `BaseRepository`.

### Principio de Segregación de Interfaces (ISP)
Las interfaces están diseñadas de manera específica para sus clientes. No forzamos a las clases a implementar métodos que no necesitan.

### Principio de Inversión de Dependencias (DIP)
Las clases de alto nivel dependen de abstracciones, no de implementaciones concretas. Por ejemplo, `VueloService` depende de `BaseRepository`, no de la implementación concreta.
