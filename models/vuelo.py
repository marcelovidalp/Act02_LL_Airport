from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import enum
import datetime

Base = declarative_base()

class TipoVuelo(enum.Enum):
    DESPEGUE = "despegue"
    ATERRIZAJE = "aterrizaje"

class PrioridadVuelo(enum.Enum):
    EMERGENCIA = "emergencia"  # Máxima prioridad
    URGENTE = "urgente"        # Alta prioridad
    REGULAR = "regular"        # Prioridad normal

class TipoEmergencia(enum.Enum):
    FALLA_TECNICA = "falla_tecnica"
    COMBUSTIBLE_BAJO = "combustible_bajo"
    EMERGENCIA_MEDICA = "emergencia_medica"
    CLIMA_ADVERSO = "clima_adverso"
    NINGUNA = "ninguna"        # Para vuelos regulares

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
    
    def __init__(self, numero_vuelo, aerolinea, origen, destino, hora_programada, 
                 tipo_vuelo, prioridad=PrioridadVuelo.REGULAR, 
                 tipo_emergencia=TipoEmergencia.NINGUNA):
        self.numero_vuelo = numero_vuelo
        self.aerolinea = aerolinea
        self.origen = origen
        self.destino = destino
        self.hora_programada = hora_programada
        self.tipo_vuelo = tipo_vuelo
        self.prioridad = prioridad
        self.tipo_emergencia = tipo_emergencia
        
    def __repr__(self):
        return f"<Vuelo {self.numero_vuelo} - {self.aerolinea} ({self.tipo_vuelo.value})>"
    
    def declarar_emergencia(self, tipo_emergencia, prioridad=PrioridadVuelo.EMERGENCIA):
        """Marca el vuelo como emergencia y establece su prioridad"""
        self.tipo_emergencia = tipo_emergencia
        self.prioridad = prioridad
        self.estado = "Emergencia"
        
    def aplicar_demora(self, minutos):
        """Aplica una demora al vuelo en minutos"""
        self.demora_minutos += minutos
        self.hora_programada = self.hora_programada + datetime.timedelta(minutes=minutos)
        self.estado = "Demorado"
