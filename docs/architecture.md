# Sistema de Gestión de Aeropuerto - Documentación de Arquitectura

## Arquitectura del Sistema

El Sistema de Gestión de Aeropuerto sigue un patrón de arquitectura por capas y modular para asegurar la separación de responsabilidades, mantenibilidad y testabilidad.

### Capas

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

```
app/
  ├── api/               # Puntos finales de API y definiciones de rutas
  │    ├── __init__.py   # Agregación de routers
  │    ├── flight_routes.py   # Puntos finales específicos de vuelos
  │    └── list_routes.py     # Puntos finales de gestión de listas
  ├── services/          # Lógica de negocio
  │    ├── __init__.py
  │    ├── flight_service.py  # Operaciones relacionadas con vuelos
  │    └── linked_list.py     # Implementación de lista doblemente enlazada
  ├── schemas/           # Validación de datos con Pydantic
  │    ├── __init__.py
  │    ├── vuelo_schemas.py   # Esquemas específicos de vuelos
  │    └── lista_schemas.py   # Esquemas específicos de listas
  ├── db/                # Configuración de base de datos
  │    ├── __init__.py
  │    └── config.py         # Configuración de conexión a base de datos
  ├── __init__.py        # Inicialización del paquete
  ├── models.py          # Modelos de base de datos usando SQLAlchemy
docs/                    # Documentación
  ├── api_documentation.md
  └── architecture.md
```

## Flujo de Datos

1. El cliente envía una petición a un punto final de la API
2. El manejador de rutas apropiado procesa la petición
3. El manejador de rutas llama a una función de servicio
4. El servicio ejecuta la lógica de negocio, frecuentemente usando funciones de acceso a datos
5. La respuesta se devuelve a través del servicio a la capa de API
6. La capa de API formatea y envía la respuesta al cliente

## Componentes Clave

### Implementación de Lista Doblemente Enlazada

El sistema utiliza una lista doblemente enlazada para gestionar vuelos, con estos componentes clave:

- **Nodo (Nodo)**: Contiene datos de vuelo y referencias a nodos anterior y siguiente
- **Lista de Vuelos (ListaVuelos)**: Contiene referencias a los nodos cabeza y cola
- **Operaciones de Lista**: Métodos para agregar, eliminar, reordenar y recorrer la lista

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

- Excepciones HTTP para errores del lado del cliente
- Gestión de transacciones de base de datos
- Manejo de excepciones para operaciones críticas

## Conclusión

Esta arquitectura proporciona una base sólida para el Sistema de Gestión de Aeropuerto, enfatizando:

- Modularidad y separación de responsabilidades
- Escalabilidad mediante diseño por capas
- Mantenibilidad con responsabilidades claras de los componentes
- Testabilidad con componentes aislados e interfaces bien definidas
