"""
Gestor de lista enlazada que conecta la implementación en memoria con los datos persistentes
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models import Vuelo, ListaVuelos, EstadoVuelo
from app.domain.memory_linked_list import MemoryLinkedList
from app.repositories.flight_repository import FlightRepository
from app.repositories.list_repository import ListRepository

class LinkedListManager:
    """
    Gestiona la lista doblemente enlazada en memoria y su sincronización con la base de datos
    """
    # Almacén en memoria de listas enlazadas - clave: lista_id, valor: instancia MemoryLinkedList
    _lists_cache: Dict[int, MemoryLinkedList[Vuelo]] = {}
    
    @classmethod
    def get_list_instance(cls, db: Session, lista_id: int) -> MemoryLinkedList[Vuelo]:
        """
        Obtiene una instancia de lista enlazada en memoria para una lista específica
        Si no existe, la crea y la llena con los vuelos de la base de datos
        """
        # Si ya está en caché, devolverla
        if lista_id in cls._lists_cache:
            return cls._lists_cache[lista_id]
        
        # Si no, crear una nueva lista y llenarla con los vuelos de la BD
        list_repo = ListRepository(db)
        flight_repo = FlightRepository(db)
        
        lista_db = list_repo.get_by_id(lista_id)
        if not lista_db:
            raise ValueError(f"Lista con ID {lista_id} no encontrada")
        
        # Crear lista en memoria
        memory_list = MemoryLinkedList[Vuelo]()
        
        # Obtener vuelos ordenados por prioridad
        vuelos = flight_repo.get_flights_by_list_id(lista_id)
        
        # Ordenar vuelos por prioridad
        vuelos_por_prioridad = {
            "emergencia": [],
            "embarque": [],
            "programado": [],
            "otros": []
        }
        
        for v in vuelos:
            if v.estado == EstadoVuelo.EMERGENCIA:
                vuelos_por_prioridad["emergencia"].append(v)
            elif v.estado == EstadoVuelo.EMBARQUE:
                vuelos_por_prioridad["embarque"].append(v)
            elif v.estado == EstadoVuelo.PROGRAMADO:
                vuelos_por_prioridad["programado"].append(v)
            else:
                vuelos_por_prioridad["otros"].append(v)
        
        # Añadir vuelos a la lista en orden de prioridad
        for v in vuelos_por_prioridad["emergencia"]:
            memory_list.add_last(v)
        for v in vuelos_por_prioridad["embarque"]:
            memory_list.add_last(v)
        for v in vuelos_por_prioridad["programado"]:
            memory_list.add_last(v)
        for v in vuelos_por_prioridad["otros"]:
            memory_list.add_last(v)
        
        # Guardar en caché
        cls._lists_cache[lista_id] = memory_list
        return memory_list
    
    @classmethod
    def clear_cache(cls, lista_id: Optional[int] = None):
        """
        Limpia la caché de listas enlazadas
        Si se proporciona lista_id, solo limpia esa lista específica
        """
        if lista_id is not None:
            if lista_id in cls._lists_cache:
                del cls._lists_cache[lista_id]
        else:
            cls._lists_cache.clear()
    
    @classmethod
    def add_first(cls, db: Session, lista_id: int, vuelo: Vuelo) -> Vuelo:
        """Añade un vuelo al principio de la lista"""
        # Asegurar que el vuelo esté en la BD y asociado a la lista
        flight_repo = FlightRepository(db)
        
        # Establecer la relación en la BD
        vuelo.lista_vuelos_id = lista_id
        flight_repo.update(vuelo)
        
        # Añadir a la lista en memoria
        memory_list = cls.get_list_instance(db, lista_id)
        memory_list.add_first(vuelo)
        
        print(f"Vuelo {vuelo.codigo} añadido al inicio de la lista {lista_id}")
        print(f"Estado actual de la lista: {memory_list.visualize()}")
        
        return vuelo

    @classmethod
    def add_last(cls, db: Session, lista_id: int, vuelo: Vuelo) -> Vuelo:
        """Añade un vuelo al final de la lista"""
        # Establecer la relación en la BD
        flight_repo = FlightRepository(db)
        vuelo.lista_vuelos_id = lista_id
        flight_repo.update(vuelo)
        
        # Añadir a la lista en memoria
        memory_list = cls.get_list_instance(db, lista_id)
        memory_list.add_last(vuelo)
        
        print(f"Vuelo {vuelo.codigo} añadido al final de la lista {lista_id}")
        print(f"Estado actual de la lista: {memory_list.visualize()}")
        
        return vuelo
    
    @classmethod
    def insert_at(cls, db: Session, lista_id: int, vuelo: Vuelo, position: int) -> Vuelo:
        """Inserta un vuelo en una posición específica"""
        # Establecer la relación en la BD
        flight_repo = FlightRepository(db)
        vuelo.lista_vuelos_id = lista_id
        flight_repo.update(vuelo)
        
        # Insertar en la lista en memoria
        memory_list = cls.get_list_instance(db, lista_id)
        memory_list.insert_at(position, vuelo)
        
        return vuelo
    
    @classmethod
    def remove_at(cls, db: Session, lista_id: int, position: int) -> Optional[Vuelo]:
        """Elimina un vuelo de una posición específica"""
        memory_list = cls.get_list_instance(db, lista_id)
        vuelo = memory_list.remove_at(position)
        
        if vuelo:
            # Actualizar en la BD
            flight_repo = FlightRepository(db)
            vuelo.lista_vuelos_id = None
            flight_repo.update(vuelo)
        
        return vuelo
    
    @classmethod
    def get_first(cls, db: Session, lista_id: int) -> Optional[Vuelo]:
        """Obtiene el primer vuelo sin eliminarlo"""
        memory_list = cls.get_list_instance(db, lista_id)
        return memory_list.get_first()
    
    @classmethod
    def get_last(cls, db: Session, lista_id: int) -> Optional[Vuelo]:
        """Obtiene el último vuelo sin eliminarlo"""
        memory_list = cls.get_list_instance(db, lista_id)
        return memory_list.get_last()
    
    @classmethod
    def get_at(cls, db: Session, lista_id: int, position: int) -> Optional[Vuelo]:
        """Obtiene un vuelo en una posición específica sin eliminarlo"""
        memory_list = cls.get_list_instance(db, lista_id)
        return memory_list.get_at(position)
    
    @classmethod
    def get_all(cls, db: Session, lista_id: int) -> List[Vuelo]:
        """Obtiene todos los vuelos de la lista"""
        memory_list = cls.get_list_instance(db, lista_id)
        return memory_list.get_all()
    
    @classmethod
    def size(cls, db: Session, lista_id: int) -> int:
        """Obtiene el tamaño de la lista"""
        memory_list = cls.get_list_instance(db, lista_id)
        return memory_list.size()
    
    @classmethod
    def prioritize(cls, db: Session, lista_id: int) -> Dict[str, int]:
        """
        Prioriza los vuelos según su estado:
        1. Emergencia
        2. Embarque
        3. Programado
        4. Otros
        """
        # Obtener todos los vuelos de la lista desde la BD
        flight_repo = FlightRepository(db)
        vuelos = flight_repo.get_flights_by_list_id(lista_id)
        
        # Clasificar por estado
        emergencias = []
        embarques = []
        programados = []
        otros = []
        
        for v in vuelos:
            if v.estado == EstadoVuelo.EMERGENCIA:
                emergencias.append(v)
            elif v.estado == EstadoVuelo.EMBARQUE:
                embarques.append(v)
            elif v.estado == EstadoVuelo.PROGRAMADO:
                programados.append(v)
            else:
                otros.append(v)
        
        # Recrear lista en memoria
        cls.clear_cache(lista_id)
        memory_list = MemoryLinkedList[Vuelo]()
        
        # Añadir en orden de prioridad
        for v in emergencias:
            memory_list.add_last(v)
        for v in embarques:
            memory_list.add_last(v)
        for v in programados:
            memory_list.add_last(v)
        for v in otros:
            memory_list.add_last(v)
        
        # Guardar en caché
        cls._lists_cache[lista_id] = memory_list
        
        return {
            "emergencias": len(emergencias),
            "embarques": len(embarques),
            "programados": len(programados),
            "otros": len(otros),
            "total": len(vuelos)
        }
