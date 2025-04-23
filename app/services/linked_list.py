"""
Operaciones de lista doblemente enlazada para la gestión de vuelos
"""
from sqlalchemy.orm import Session
from app.models import Vuelo, Nodo, ListaVuelos, EstadoVuelo

def add_first(db: Session, lista: ListaVuelos, vuelo: Vuelo):
    """
    Añade un vuelo al principio de la lista.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        vuelo: El vuelo a añadir
        
    Returns:
        El nodo creado
    """
    nuevo_nodo = Nodo(vuelo=vuelo)
    db.add(nuevo_nodo)
    db.flush()  # Para obtener el ID del nuevo nodo
    
    if not lista.cabeza:
        lista.cabeza = nuevo_nodo
        lista.cola = nuevo_nodo
    else:
        nuevo_nodo.siguiente = lista.cabeza
        lista.cabeza.anterior = nuevo_nodo
        lista.cabeza = nuevo_nodo
    
    return nuevo_nodo

def add_last(db: Session, lista: ListaVuelos, vuelo: Vuelo):
    """
    Añade un vuelo al final de la lista.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        vuelo: El vuelo a añadir
        
    Returns:
        El nodo creado
    """
    nuevo_nodo = Nodo(vuelo=vuelo)
    db.add(nuevo_nodo)
    db.flush()
    
    if not lista.cola:
        lista.cabeza = nuevo_nodo
        lista.cola = nuevo_nodo
    else:
        nuevo_nodo.anterior = lista.cola
        lista.cola.siguiente = nuevo_nodo
        lista.cola = nuevo_nodo
    
    return nuevo_nodo

def remove_first(db: Session, lista: ListaVuelos):
    """
    Elimina el primer vuelo de la lista.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        
    Returns:
        El vuelo eliminado o None si la lista está vacía
    """
    if not lista.cabeza:
        return None
    
    nodo_eliminado = lista.cabeza
    
    if lista.cabeza == lista.cola:
        lista.cabeza = None
        lista.cola = None
    else:
        lista.cabeza = nodo_eliminado.siguiente
        lista.cabeza.anterior = None
    
    db.delete(nodo_eliminado)
    return nodo_eliminado.vuelo

def remove_last(db: Session, lista: ListaVuelos):
    """
    Elimina el último vuelo de la lista.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        
    Returns:
        El vuelo eliminado o None si la lista está vacía
    """
    if not lista.cola:
        return None
    
    nodo_eliminado = lista.cola
    
    if lista.cabeza == lista.cola:
        lista.cabeza = None
        lista.cola = None
    else:
        lista.cola = nodo_eliminado.anterior
        lista.cola.siguiente = None
    
    db.delete(nodo_eliminado)
    return nodo_eliminado.vuelo

def prioritize_flights(db: Session, lista: ListaVuelos):
    """
    Reorganiza la lista según la prioridad del estado de los vuelos.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        
    Returns:
        Mensaje con información sobre la priorización
    """
    # Crear listas temporales para cada categoría
    emergencias = []
    embarques = []
    programados = []
    otros = []
    
    # Recorrer la lista actual y clasificar los vuelos
    nodo_actual = lista.cabeza
    while nodo_actual:
        vuelo = nodo_actual.vuelo
        if vuelo.estado == EstadoVuelo.EMERGENCIA:
            emergencias.append(vuelo)
        elif vuelo.estado == EstadoVuelo.EMBARQUE:
            embarques.append(vuelo)
        elif vuelo.estado == EstadoVuelo.PROGRAMADO:
            programados.append(vuelo)
        else:
            otros.append(vuelo)
        
        nodo_actual = nodo_actual.siguiente
    
    # Vaciar la lista actual
    while lista.cabeza:
        remove_first(db, lista)
    
    # Reconstruir la lista con el nuevo orden
    for v in emergencias:
        add_last(db, lista, v)
    for v in embarques:
        add_last(db, lista, v)
    for v in programados:
        add_last(db, lista, v)
    for v in otros:
        add_last(db, lista, v)
    
    return {
        "mensaje": f"Lista priorizada: {len(emergencias)} emergencias, {len(embarques)} embarques, {len(programados)} programados, {len(otros)} otros"
    }

def get_length(lista: ListaVuelos):
    """
    Obtiene la longitud de la lista.
    
    Args:
        lista: La lista de vuelos
        
    Returns:
        El número de vuelos en la lista
    """
    count = 0
    nodo_actual = lista.cabeza
    while nodo_actual:
        count += 1
        nodo_actual = nodo_actual.siguiente
    return count

def get_first(lista: ListaVuelos):
    """
    Obtiene el primer vuelo sin eliminarlo.
    
    Args:
        lista: La lista de vuelos
        
    Returns:
        El primer vuelo o None si la lista está vacía
    """
    if not lista.cabeza:
        return None
    return lista.cabeza.vuelo

def get_last(lista: ListaVuelos):
    """
    Obtiene el último vuelo sin eliminarlo.
    
    Args:
        lista: La lista de vuelos
        
    Returns:
        El último vuelo o None si la lista está vacía
    """
    if not lista.cola:
        return None
    return lista.cola.vuelo

def add_at_position(db: Session, lista: ListaVuelos, vuelo: Vuelo, position: int):
    """
    Inserta un vuelo en una posición específica.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        vuelo: El vuelo a insertar
        position: Posición donde insertar (indexado en 0)
        
    Returns:
        El nodo insertado
    """
    # Si la posición es 0 o la lista está vacía, insertar al principio
    if position <= 0 or not lista.cabeza:
        return add_first(db, lista, vuelo)
    
    # Obtener longitud de la lista
    length = get_length(lista)
    
    # Si la posición es más allá del final, insertar al final
    if position >= length:
        return add_last(db, lista, vuelo)
    
    # Encontrar la posición
    current = lista.cabeza
    for _ in range(position):
        current = current.siguiente
    
    # Crear nuevo nodo
    new_node = Nodo(vuelo=vuelo)
    db.add(new_node)
    db.flush()
    
    # Actualizar enlaces
    new_node.anterior = current.anterior
    new_node.siguiente = current
    current.anterior.siguiente = new_node
    current.anterior = new_node
    
    return new_node

def remove_at_position(db: Session, lista: ListaVuelos, position: int):
    """
    Elimina un vuelo de una posición específica.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        position: Posición de donde eliminar (indexado en 0)
        
    Returns:
        El vuelo eliminado o None si la posición es inválida
    """
    # Si la lista está vacía
    if not lista.cabeza:
        return None
    
    # Si se elimina desde el principio
    if position == 0:
        return remove_first(db, lista)
    
    # Obtener longitud de la lista
    length = get_length(lista)
    
    # Si la posición es la última
    if position >= length - 1:
        return remove_last(db, lista)
    
    # Encontrar la posición
    current = lista.cabeza
    for _ in range(position):
        current = current.siguiente
    
    # Actualizar enlaces
    current.anterior.siguiente = current.siguiente
    current.siguiente.anterior = current.anterior
    
    # Guardar vuelo antes de eliminar el nodo
    flight = current.vuelo
    
    # Eliminar nodo
    db.delete(current)
    
    return flight

def get_all_flights(lista: ListaVuelos):
    """
    Recorre toda la lista y devuelve todos los vuelos.
    
    Args:
        lista: La lista de vuelos
        
    Returns:
        Lista de todos los vuelos en la lista
    """
    flights = []
    current = lista.cabeza
    while current:
        flights.append(current.vuelo)
        current = current.siguiente
    return flights

def reorder_flight(db: Session, lista: ListaVuelos, from_pos: int, to_pos: int):
    """
    Reordena un vuelo moviéndolo de una posición a otra.
    
    Args:
        db: Sesión de base de datos
        lista: La lista de vuelos
        from_pos: Posición de origen (indexado en 0)
        to_pos: Posición de destino (indexado en 0)
        
    Returns:
        El vuelo reordenado o None si las posiciones son inválidas
    """
    # Casos extremos
    if from_pos == to_pos or not lista.cabeza:
        return None
    
    # Obtener longitud de la lista
    length = get_length(lista)
    if from_pos < 0 or from_pos >= length or to_pos < 0:
        return None
    
    # Extraer vuelo de la posición de origen
    flight = remove_at_position(db, lista, from_pos)
    if not flight:
        return None
    
    # Ajustar posición de destino si es necesario (ya que eliminamos un elemento)
    if to_pos > from_pos:
        to_pos -= 1
    
    # Insertar vuelo en la posición de destino
    add_at_position(db, lista, flight, to_pos)
    return flight
