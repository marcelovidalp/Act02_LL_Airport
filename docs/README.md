# Sistema de Gestión de Aeropuerto

## Descripción General
Este proyecto implementa un sistema de gestión para secuencias de vuelos en un aeropuerto, utilizando una lista doblemente enlazada con nodos centinela (header y trailer) para administrar eficientemente la cola de despegues y aterrizajes.

## Características Principales
- Gestión de secuencias de vuelos (despegues y aterrizajes)
- Priorización de vuelos según su estado (emergencias, vuelos regulares)
- Manejo de demoras y reprogramaciones
- API REST para interactuar con el sistema

## Tecnologías Utilizadas
- **Python**: Lenguaje de programación principal
- **FastAPI**: Framework para la creación de API RESTful
- **SQLAlchemy**: ORM para la persistencia de datos
- **MySQL**: Sistema de gestión de base de datos relacional

## Arquitectura
El proyecto sigue una arquitectura por capas con los siguientes componentes:

1. **Capa de Datos**: Modelos ORM y repositorios
2. **Capa de Dominio**: Lógica de negocio e implementación de la lista enlazada
3. **Capa de Servicios**: Coordinación entre repositorios y operaciones de negocio
4. **Capa de API**: Endpoints REST para interactuar con el sistema

## Patrones de Diseño
- **Repository**: Abstracción de acceso a datos
- **Dependency Injection**: Inyección de dependencias para facilitar pruebas y flexibilidad
- **Strategy**: Diferentes estrategias para ordenamiento de vuelos

## Documentación Adicional
- [Arquitectura Detallada](arquitectura.md)
- [Modelos de Datos](modelos.md)
- [Lista Doblemente Enlazada](lista_enlazada.md)
- [API y Endpoints](api_endpoints.md)
- [Patrones de Diseño](patrones.md)
