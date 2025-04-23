# Documentación de la API del Sistema de Gestión de Aeropuerto

## Descripción General

Esta API gestiona los vuelos de un aeropuerto utilizando una estructura de datos de lista doblemente enlazada. Permite operaciones 
como añadir, eliminar y reordenar vuelos, así como priorizarlos según su estado.

## Arquitectura

El sistema sigue una arquitectura por capas:

1. **Capa de API** - Endpoints FastAPI para operaciones con vuelos
2. **Capa de Servicio** - Lógica de negocio y operaciones sobre la lista enlazada
3. **Capa de Datos** - Modelos SQLAlchemy y operaciones de base de datos

## Implementación de Lista Enlazada

Los vuelos están organizados en una lista doblemente enlazada donde:
- Cada nodo contiene un vuelo y punteros a los nodos anterior y siguiente
- La lista mantiene punteros a cabeza y cola para operaciones eficientes
- Las operaciones incluyen inserción/eliminación en ambos extremos y en posiciones específicas

## Endpoints Disponibles

### Información de Vuelos

- `GET /api/vuelos/`: Lista todos los vuelos en la base de datos
- `GET /api/vuelos/{vuelo_id}`: Obtiene detalles de un vuelo específico
- `POST /api/vuelos/`: Crea un nuevo vuelo
- `PATCH /api/vuelos/{vuelo_id}/estado`: Actualiza el estado de un vuelo

### Operaciones de Lista Enlazada

- `GET /api/vuelos/total`: Obtiene el número total de vuelos en la lista
- `GET /api/vuelos/proximo`: Obtiene el próximo vuelo (primero en la lista)
- `GET /api/vuelos/ultimo`: Obtiene el último vuelo en la lista
- `GET /api/vuelos/lista`: Obtiene todos los vuelos recorriendo la lista enlazada
- `POST /api/vuelos`: Añade un vuelo al principio o al final de la lista
- `POST /api/vuelos/insertar`: Inserta un vuelo en una posición específica
- `DELETE /api/vuelos/extraer`: Extrae un vuelo de una posición específica
- `PATCH /api/vuelos/reordenar`: Reordena un vuelo moviéndolo de una posición a otra
- `POST /api/listas/{lista_id}/priorizar`: Prioriza los vuelos según su estado

## Estados de Vuelo

- `PROGRAMADO`: Vuelo programado
- `EMBARQUE`: Vuelo en embarque
- `DESPEGADO`: Vuelo despegado
- `ATERRIZADO`: Vuelo aterrizado
- `RETRASADO`: Vuelo retrasado
- `EMERGENCIA`: Vuelo en emergencia (máxima prioridad)
- `CANCELADO`: Vuelo cancelado

## Ejemplo de Uso

### Añadir un vuelo al principio de la lista

```http
POST /api/vuelos
Content-Type: application/json

{
  "codigo": "IB3456",
  "origen": "Madrid",
  "destino": "Barcelona",
  "estado": "programado",
  "aerolinea": "Iberia"
}
```

Parámetro de consulta: `?position=first`

### Priorizar vuelos

```http
POST /api/listas/1/priorizar
```

Esto reorganiza la lista según la prioridad del estado de los vuelos: 
primero vuelos en emergencia, luego vuelos en embarque, luego vuelos programados y finalmente otros.
