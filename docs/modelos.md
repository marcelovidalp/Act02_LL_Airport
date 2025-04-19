# Modelos de Datos

## Descripción General
Los modelos de datos constituyen la base del sistema y definen la estructura de la información con la que trabaja la aplicación. Utilizamos SQLAlchemy como ORM para modelar y persistir los datos en MySQL.

## Modelo de Vuelo

### Enumeraciones
El modelo de vuelo utiliza varias enumeraciones para establecer valores constantes y restringidos:

#### TipoVuelo
```python
class TipoVuelo(enum.Enum):
    DESPEGUE = "despegue"
    ATERRIZAJE = "aterrizaje"
```
Esta enumeración distingue entre vuelos de despegue y aterrizaje, lo que ayuda a categorizarlos en las colas adecuadas.

#### PrioridadVuelo
```python
class PrioridadVuelo(enum.Enum):
    EMERGENCIA = "emergencia"  # Máxima prioridad
    URGENTE = "urgente"        # Alta prioridad
    REGULAR = "regular"        # Prioridad normal
```
Define los niveles de prioridad para los vuelos, afectando directamente su posición en la cola.

#### TipoEmergencia
```python
class TipoEmergencia(enum.Enum):
    FALLA_TECNICA = "falla_tecnica"
    COMBUSTIBLE_BAJO = "combustible_bajo"
    EMERGENCIA_MEDICA = "emergencia_medica"
    CLIMA_ADVERSO = "clima_adverso"
    NINGUNA = "ninguna"        # Para vuelos regulares
```
Especifica los tipos de emergencias que pueden afectar a un vuelo, utilizado cuando un vuelo se declara en estado de emergencia.

### Clase Vuelo
La clase `Vuelo` es el modelo principal que representa un vuelo en el sistema:

```python
class Vuelo(Base):
    __tablename__ = 'vuelos'
    
    id = Column(Integer, primary_key=True)
    numero_vuelo = Column(String(20), nullable=False, unique=True)
    aerolinea = Column(String(100), nullable=False)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    hora_programada = Column(DateTime, nullable=False)
    tipo_vuelo = Column(Enum(TipoVuelo), nullable=False)
    prioridad = Column(Enum(PrioridadVuelo), default=PrioridadVuelo.REGULAR)
    tipo_emergencia = Column(Enum(TipoEmergencia), default=TipoEmergencia.NINGUNA)
    estado = Column(String(50), default="Programado")
    demora_minutos = Column(Integer, default=0)
```

#### Atributos principales:
- **id**: Identificador único del vuelo
- **numero_vuelo**: Código alfanumérico que identifica el vuelo (ej. "AA123")
- **aerolinea**: Nombre de la aerolínea
- **origen/destino**: Ciudades de origen y destino
- **hora_programada**: Fecha y hora programadas para el vuelo
- **tipo_vuelo**: Si es despegue o aterrizaje
- **prioridad**: Nivel de prioridad actual del vuelo
- **tipo_emergencia**: Tipo de emergencia si existe
- **estado**: Estado actual del vuelo ("Programado", "Emergencia", "Demorado", etc.)
- **demora_minutos**: Minutos de retraso acumulados

### Métodos Principales

#### Constructor
```python
def __init__(self, numero_vuelo, aerolinea, origen, destino, hora_programada, 
             tipo_vuelo, prioridad=PrioridadVuelo.REGULAR, 
             tipo_emergencia=TipoEmergencia.NINGUNA):
    # Inicialización de atributos
```
Inicializa un nuevo vuelo con los parámetros proporcionados, estableciendo valores por defecto para la prioridad y tipo de emergencia.

#### declarar_emergencia
```python
def declarar_emergencia(self, tipo_emergencia, prioridad=PrioridadVuelo.EMERGENCIA):
    """Marca el vuelo como emergencia y establece su prioridad"""
    self.tipo_emergencia = tipo_emergencia
    self.prioridad = prioridad
    self.estado = "Emergencia"
```
Actualiza el estado de un vuelo a emergencia, estableciendo el tipo específico de emergencia y modificando su prioridad.

#### aplicar_demora
```python
def aplicar_demora(self, minutos):
    """Aplica una demora al vuelo en minutos"""
    self.demora_minutos += minutos
    self.hora_programada = self.hora_programada + datetime.timedelta(minutes=minutos)
    self.estado = "Demorado"
```
Registra una demora para el vuelo, actualizando tanto el contador de minutos de demora como la hora programada estimada.

## Diagrama de Relaciones

En este sistema, la entidad principal es `Vuelo`, que se relaciona con las enumeraciones que restringen sus valores:

```
+----------------+     +----------------+     +----------------+
| TipoVuelo      |     | PrioridadVuelo |     | TipoEmergencia |
+----------------+     +----------------+     +----------------+
| DESPEGUE       |     | EMERGENCIA     |     | FALLA_TECNICA  |
| ATERRIZAJE     |     | URGENTE        |     | COMBUSTIBLE    |
+----------------+     | REGULAR        |     | MEDICA         |
        ^               +----------------+     | CLIMA          |
        |                      ^               | NINGUNA        |
        |                      |               +----------------+
        |                      |                      ^
        |                      |                      |
+--------------------------------------------------------------------------------+
| Vuelo                                                                          |
+--------------------------------------------------------------------------------+
| id: Integer                                                                    |
| numero_vuelo: String                                                           |
| aerolinea: String                                                              |
| origen: String                                                                 |
| destino: String                                                                |
| hora_programada: DateTime                                                      |
| tipo_vuelo: TipoVuelo                                                          |
| prioridad: PrioridadVuelo                                                      |
| tipo_emergencia: TipoEmergencia                                                |
| estado: String                                                                 |
| demora_minutos: Integer                                                        |
+--------------------------------------------------------------------------------+
```

## Impacto en el Rendimiento
El modelo está diseñado para facilitar las consultas sobre vuelos según su estado, prioridad y tipo, aspectos fundamentales para el sistema. La unicidad del campo `numero_vuelo` asegura que no haya duplicados en el sistema, mientras que los campos indexados mejoran el rendimiento de las búsquedas frecuentes.
