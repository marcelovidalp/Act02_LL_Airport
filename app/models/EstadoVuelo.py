import enum

class EstadoVuelo(enum.Enum):
    PROGRAMADO = "programado"
    EMBARQUE = "embarque"
    DESPEGADO = "despegado"
    ATERRIZADO = "aterrizado"
    RETRASADO = "retrasado"
    EMERGENCIA = "emergencia"
    CANCELADO = "cancelado"