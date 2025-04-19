from typing import List, Optional
from ..repositories.vuelo_repository import VueloRepository
from ..domain.linked_list.double_linked_list import DoubleLinkedList
from ..models.vuelo import Vuelo, PrioridadVuelo, TipoEmergencia
from datetime import datetime

class VueloService:
    """Servicio para gestionar vuelos y su prioridad"""
    
    def __init__(self, repository: VueloRepository):
        self.repository = repository
        # Inicializar listas para despegues y aterrizajes
        self.cola_despegues = DoubleLinkedList()
        self.cola_aterrizajes = DoubleLinkedList()
        self._cargar_vuelos_desde_db()
        
    def _cargar_vuelos_desde_db(self):
        """Carga los vuelos desde la base de datos a las listas"""
        vuelos = self.repository.get_all()
        for vuelo in vuelos:
            if vuelo.tipo_vuelo.value == "despegue":
                self.cola_despegues.insert_by_priority(vuelo)
            else:  # aterrizaje
                self.cola_aterrizajes.insert_by_priority(vuelo)
    
    def agregar_vuelo(self, vuelo: Vuelo) -> Vuelo:
        """Agrega un nuevo vuelo al sistema"""
        # Guardar en la base de datos
        vuelo_guardado = self.repository.add(vuelo)
        
        # Agregar a la cola correspondiente según el tipo
        if vuelo.tipo_vuelo.value == "despegue":
            self.cola_despegues.insert_by_priority(vuelo_guardado)
        else:  # aterrizaje
            self.cola_aterrizajes.insert_by_priority(vuelo_guardado)
            
        return vuelo_guardado
    
    def declarar_emergencia(self, numero_vuelo: str, tipo_emergencia: TipoEmergencia) -> Optional[Vuelo]:
        """Declara una emergencia para un vuelo específico"""
        vuelo = self.repository.get_by_numero_vuelo(numero_vuelo)
        if not vuelo:
            return None
            
        # Actualizar estado en la base de datos
        vuelo.declarar_emergencia(tipo_emergencia)
        self.repository.update(vuelo)
        
        # Reordenar las colas para reflejar la nueva prioridad
        if vuelo.tipo_vuelo.value == "despegue":
            self.cola_despegues.reorder_by_priority()
        else:
            self.cola_aterrizajes.reorder_by_priority()
            
        return vuelo
    
    def aplicar_demora(self, numero_vuelo: str, minutos: int) -> Optional[Vuelo]:
        """Aplica una demora a un vuelo y reordena la cola si es necesario"""
        vuelo = self.repository.get_by_numero_vuelo(numero_vuelo)
        if not vuelo:
            return None
        
        # Aplicar la demora
        vuelo.aplicar_demora(minutos)
        self.repository.update(vuelo)
        
        # Reordenar puede ser necesario si las demoras afectan la prioridad
        # (por ejemplo, si tenemos una lógica que cambia prioridades según el tiempo)
        return vuelo
    
    def obtener_proximo_vuelo(self, tipo: str) -> Optional[Vuelo]:
        """Obtiene el próximo vuelo en la cola según el tipo"""
        cola = self.cola_despegues if tipo == "despegue" else self.cola_aterrizajes
        
        if cola.is_empty():
            return None
            
        # El próximo vuelo es el primero después del header
        return cola.header.next.vuelo
