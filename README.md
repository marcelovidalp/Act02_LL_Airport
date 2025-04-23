# Sistema de Gestión de Aeropuerto

Este proyecto implementa un sistema de gestión de vuelos para aeropuertos utilizando una estructura de datos de lista doblemente enlazada. El sistema está desarrollado con FastAPI y SQLAlchemy, siguiendo una arquitectura modular y por capas.

## Características Principales

- Gestión completa de vuelos con diversos estados (programado, embarque, emergencia, etc.)
- Implementación de lista doblemente enlazada para organizar los vuelos con eficiencia
- Priorización automática de vuelos según su estado
- API RESTful completa para todas las operaciones
- Documentación detallada para explicar la arquitectura y funcionalidades

## Estructura del Proyecto

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
  ├── models/            # Modelos de base de datos
  │    ├── Base.py
  │    ├── EstadoVuelo.py
  │    ├── ListaVuelos.py
  │    ├── Nodo.py
  │    └── Vuelo.py
  ├── __init__.py        # Inicialización del paquete
docs/                    # Documentación
  ├── api_documentation.md   # Documentación detallada de la API
  ├── architecture.md        # Descripción de la arquitectura del sistema
  ├── visual_guides.md       # Visualizaciones de la estructura de datos
  └── demo_scenarios.md      # Escenarios de uso para demostraciones
```

## Requisitos

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/yourusername/Act02_LL_Airport.git
   cd Act02_LL_Airport
   ```

2. **Crear y activar entorno virtual:**

   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

1. **Iniciar el servidor:**

   ```bash
   python main.py
   ```

   El servidor se ejecutará en `http://localhost:8000`.

2. **Acceder a la documentación de la API:**

   Abra en su navegador: `http://localhost:8000/docs`

## Estructura de Datos: Lista Doblemente Enlazada

El sistema utiliza una lista doblemente enlazada para organizar los vuelos de manera eficiente, permitiendo:

- Inserción rápida al principio y al final (O(1))
- Eliminación rápida al principio y al final (O(1))
- Priorización inteligente por estado de vuelo
- Reorganización dinámica para manejar emergencias

Para más detalles sobre la implementación y visualización de la lista doblemente enlazada, consulte [Visual Guides](docs/visual_guides.md).

## Estados de Vuelos

Los vuelos pueden tener los siguientes estados:

- **PROGRAMADO**: Vuelo programado (estado predeterminado)
- **EMBARQUE**: Vuelo en proceso de embarque
- **DESPEGADO**: Vuelo que ha despegado
- **ATERRIZADO**: Vuelo que ha aterrizado
- **RETRASADO**: Vuelo con retraso
- **EMERGENCIA**: Vuelo en situación de emergencia (máxima prioridad)
- **CANCELADO**: Vuelo cancelado

## Endpoints Principales

- `GET /api/vuelos/`: Lista todos los vuelos
- `POST /api/vuelos/`: Crea un nuevo vuelo
- `GET /api/vuelos/{vuelo_id}`: Obtiene detalles de un vuelo específico
- `PATCH /api/vuelos/{vuelo_id}/estado`: Actualiza el estado de un vuelo
- `GET /api/vuelos/lista`: Obtiene todos los vuelos en orden de la lista
- `POST /api/listas/{lista_id}/priorizar`: Prioriza los vuelos según su estado

Para una lista completa de endpoints disponibles, consulte la [Documentación de la API](docs/api_documentation.md).

## Escenarios de Demostración

Para ver ejemplos de cómo usar el sistema en diferentes escenarios, consulte los [Escenarios de Demostración](docs/demo_scenarios.md).

## Arquitectura

Este proyecto sigue una arquitectura por capas con separación clara de responsabilidades. Para más detalles sobre la arquitectura del sistema, consulte la [Documentación de Arquitectura](docs/architecture.md).

## Contribuir

1. Haga un fork del repositorio
2. Cree una nueva rama (`git checkout -b feature/amazing-feature`)
3. Haga commit de sus cambios (`git commit -m 'Add some amazing feature'`)
4. Haga push a la rama (`git push origin feature/amazing-feature`)
5. Abra un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo LICENSE para más detalles.

