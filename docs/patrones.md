# Patrones de Diseño

## Descripción General
Este proyecto implementa varios patrones de diseño para mejorar la modularidad, extensibilidad y mantenibilidad del código. A continuación se detallan los principales patrones utilizados y su implementación concreta en el sistema.

## Patrón Repository

### Descripción
El patrón Repository actúa como una capa de abstracción entre la lógica de negocio y la fuente de datos, ocultando la complejidad de las operaciones de acceso a datos. Proporciona una interfaz unificada para trabajar con entidades de dominio.

### Implementación

#### BaseRepository (Clase abstracta)
```python
class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: Any) -> bool:
        pass
```

Esta clase define la interfaz común para todos los repositorios, con métodos genéricos CRUD.

#### VueloRepository (Implementación concreta)
```python
class VueloRepository(BaseRepository[Vuelo]):
    def __init__(self, session: Session):
        self.session = session
        
    def get_by_id(self, id: int) -> Optional[Vuelo]:
        return self.session.query(Vuelo).filter(Vuelo.id == id).first()
    
    # ...otros métodos implementados
```

La implementación concreta para `Vuelo` utiliza SQLAlchemy para realizar operaciones de base de datos.

### Beneficios
- **Desacoplamiento**: La lógica de negocio no depende directamente de SQLAlchemy o MySQL
- **Pruebas simplificadas**: Facilita la creación de mocks para pruebas unitarias
- **Consistencia**: Proporciona un conjunto estándar de operaciones para todas las entidades

## Inyección de Dependencias

### Descripción
La inyección de dependencias (DI) es un patrón que permite proporcionar a un objeto sus dependencias en lugar de que el objeto las cree internamente. Esto mejora la flexibilidad y facilita las pruebas.

### Implementación
En el proyecto, utilizamos FastAPI para la inyección de dependencias a nivel de ruta:

```python
def get_vuelo_service(db: Session = Depends(get_db)):
    repository = VueloRepository(db)
    return VueloService(repository)

@router.post("/", response_model=Vuelo)
def crear_vuelo(vuelo_create: VueloCreate, service: VueloService = Depends(get_vuelo_service)):
    # Lógica del endpoint
```

Aquí, la función `get_vuelo_service` crea y proporciona una instancia de `VueloService` con su dependencia `VueloRepository`, que a su vez recibe una sesión de base de datos.

### Beneficios
- **Desacoplamiento**: Las clases no dependen de implementaciones concretas
- **Pruebas simplificadas**: Facilita la sustitución de implementaciones reales con mocks
- **Flexibilidad**: Permite cambiar el comportamiento sin modificar las clases

## Patrón Strategy (implícito)

### Descripción
El patrón Strategy encapsula algoritmos en clases separadas y los hace intercambiables. Aunque no está implementado de manera explícita con clases separadas, el sistema utiliza un enfoque similar para los algoritmos de ordenamiento de vuelos.

### Implementación Implícita
La clase `DoubleLinkedList` implementa diferentes estrategias para insertar vuelos:

```python
def insert_by_priority(self, vuelo):
    if vuelo.prioridad == PrioridadVuelo.EMERGENCIA:
        return self.add_first(vuelo)
        
    if vuelo.prioridad == PrioridadVuelo.REGULAR:
        return self.add_last(vuelo)
        
    # Estrategia para vuelos urgentes
    # ...código para inserción en posición intermedia
```

### Beneficios
- **Extensibilidad**: Facilita la adición de nuevas estrategias de priorización
- **Mantenibilidad**: Separa diferentes algoritmos de ordenación
- **Claridad**: Hace explícitas las reglas de negocio para la priorización

## Aplicación de Principios SOLID

Los patrones implementados apoyan directamente los principios SOLID:

### Principio de Responsabilidad Única (SRP)
Cada clase tiene una única razón para cambiar. Por ejemplo:
- `VueloRepository` solo se encarga de las operaciones de persistencia
- `VueloService` maneja la lógica de negocio
- Los controladores de API solo gestionan la interacción HTTP

### Principio Abierto/Cerrado (OCP)
El sistema está diseñado para ser extendido sin modificar código existente:
- Nuevos tipos de repositorios pueden implementar `BaseRepository`
- Nuevas estrategias de priorización pueden añadirse sin modificar la estructura existente

### Principio de Sustitución de Liskov (LSP)
Las clases derivadas pueden sustituir a sus clases base:
- Cualquier `BaseRepository` puede ser utilizado donde se espera un repositorio genérico

### Principio de Segregación de Interfaces (ISP)
Las interfaces están diseñadas para ser específicas:
- `BaseRepository` define solo las operaciones esenciales
- Las implementaciones específicas pueden añadir métodos adicionales según sea necesario

### Principio de Inversión de Dependencias (DIP)
Las clases dependen de abstracciones, no de implementaciones concretas:
- `VueloService` depende de `BaseRepository`, no de `VueloRepository`
- FastAPI facilita la inyección de dependencias para mantener este principio
