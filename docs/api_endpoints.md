# API y Endpoints

## Descripción General
El sistema expone una API RESTful construida con FastAPI para permitir la interacción con el sistema de gestión de vuelos. La API facilita operaciones como crear vuelos, declarar emergencias, aplicar demoras y consultar el estado de las colas.

## Tecnologías Utilizadas
- **FastAPI**: Framework moderno para API RESTful en Python
- **Pydantic**: Validación de datos y serialización
- **SQLAlchemy**: ORM para interacción con la base de datos
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación

## Esquemas de Datos

### Esquemas Pydantic
Los esquemas Pydantic definen la estructura de los datos que se intercambian a través de la API:

#### VueloBase
```python
class VueloBase(BaseModel):
    numero_vuelo: str = Field(..., example="AA123")
    aerolinea: str = Field(..., example="American Airlines")
    origen: str = Field(..., example="Nueva York")
    destino: str = Field(..., example="Miami")
    hora_programada: datetime
    tipo_vuelo: TipoVueloSchema
    prioridad: PrioridadVueloSchema = PrioridadVueloSchema.REGULAR
    tipo_emergencia: TipoEmergenciaSchema = TipoEmergenciaSchema.NINGUNA
```

Este esquema base define los campos comunes para la creación y respuesta de vuelos.

#### Esquemas específicos
- `VueloCreate`: Para crear nuevos vuelos (hereda de VueloBase)
- `VueloUpdate`: Para actualizar vuelos existentes (todos los campos opcionales)
- `EmergenciaDeclaracion`: Para declarar emergencias
- `DemoraAplicacion`: Para aplicar demoras

## Endpoints Principales

### Crear Vuelo
```
POST /vuelos/
```

Este endpoint permite crear un nuevo vuelo en el sistema.

**Cuerpo de la solicitud**:
```json
{
  "numero_vuelo": "AA123",
  "aerolinea": "American Airlines",
  "origen": "Nueva York",
  "destino": "Miami",
  "hora_programada": "2023-11-01T12:00:00Z",
  "tipo_vuelo": "despegue",
  "prioridad": "regular",
  "tipo_emergencia": "ninguna"
}
```

**Código de implementación**:
```python
@router.post("/", response_model=Vuelo, status_code=status.HTTP_201_CREATED)
def crear_vuelo(vuelo_create: VueloCreate, service: VueloService = Depends(get_vuelo_service)):
    """Crea un nuevo vuelo en el sistema"""
    # Convertir del esquema Pydantic al modelo SQLAlchemy
    vuelo_db = VueloModel(
        numero_vuelo=vuelo_create.numero_vuelo,
        aerolinea=vuelo_create.aerolinea,
        origen=vuelo_create.origen,
        destino=vuelo_create.destino,
        hora_programada=vuelo_create.hora_programada,
        tipo_vuelo=TipoVuelo(vuelo_create.tipo_vuelo.value),
        prioridad=PrioridadVuelo(vuelo_create.prioridad.value),
        tipo_emergencia=TipoEmergencia(vuelo_create.tipo_emergencia.value)
    )
    
    # Agregar el vuelo usando el servicio
    return service.agregar_vuelo(vuelo_db)
```

### Declarar Emergencia
```
POST /vuelos/{numero_vuelo}/emergencia
```

Este endpoint permite declarar una emergencia para un vuelo existente.

**Cuerpo de la solicitud**:
```json
{
  "tipo_emergencia": "combustible_bajo"
}
```

**Código de implementación**:
```python
@router.post("/{numero_vuelo}/emergencia", response_model=Vuelo)
def declarar_emergencia(numero_vuelo: str, emergencia: EmergenciaDeclaracion, 
                        service: VueloService = Depends(get_vuelo_service)):
    """Declara una emergencia para un vuelo"""
    vuelo = service.declarar_emergencia(numero_vuelo, TipoEmergencia(emergencia.tipo_emergencia.value))
    if not vuelo:
        raise HTTPException(status_code=404, detail=f"Vuelo {numero_vuelo} no encontrado")
    return vuelo
```

### Aplicar Demora
```
POST /vuelos/{numero_vuelo}/demora
```

Este endpoint permite aplicar una demora a un vuelo existente.

**Cuerpo de la solicitud**:
```json
{
  "minutos": 30
}
```

**Código de implementación**:
```python
@router.post("/{numero_vuelo}/demora", response_model=Vuelo)
def aplicar_demora(numero_vuelo: str, demora: DemoraAplicacion,
                   service: VueloService = Depends(get_vuelo_service)):
    """Aplica una demora a un vuelo"""
    vuelo = service.aplicar_demora(numero_vuelo, demora.minutos)
    if not vuelo:
        raise HTTPException(status_code=404, detail=f"Vuelo {numero_vuelo} no encontrado")
    return vuelo
```

### Obtener Próximo Vuelo
```
GET /vuelos/proximo/{tipo}
```

Este endpoint permite obtener el próximo vuelo en la cola según el tipo (despegue o aterrizaje).

**Código de implementación**:
```python
@router.get("/proximo/{tipo}", response_model=Vuelo)
def obtener_proximo_vuelo(tipo: str, service: VueloService = Depends(get_vuelo_service)):
    """Obtiene el próximo vuelo en la cola según el tipo (despegue/aterrizaje)"""
    if tipo not in ["despegue", "aterrizaje"]:
        raise HTTPException(status_code=400, detail="Tipo debe ser 'despegue' o 'aterrizaje'")
        
    vuelo = service.obtener_proximo_vuelo(tipo)
    if not vuelo:
        raise HTTPException(status_code=404, detail=f"No hay vuelos pendientes de {tipo}")
    return vuelo
```

## Documentación Automática

FastAPI genera automáticamente documentación interactiva para la API:

- **Swagger UI**: Disponible en `/docs`
- **ReDoc**: Disponible en `/redoc`

Estas interfaces permiten explorar y probar los endpoints directamente desde el navegador.

## Gestión de Errores

La API implementa un manejo de errores estandarizado:

- **404 Not Found**: Para recursos no encontrados
- **400 Bad Request**: Para solicitudes con datos inválidos
- **500 Internal Server Error**: Para errores no controlados

Ejemplo de manejo de error:
```python
if not vuelo:
    raise HTTPException(status_code=404, detail=f"Vuelo {numero_vuelo} no encontrado")
```

## Seguridad y Validación

La API utiliza Pydantic para validación de datos, lo que garantiza:

1. **Tipos de datos correctos**: Validación automática de tipos
2. **Restricciones de campo**: Validación de longitud, formato, etc.
3. **Valores predeterminados**: Configuración automática de valores por defecto

Esto reduce significativamente la cantidad de código necesario para validar las entradas del usuario y mejora la seguridad general de la API.
