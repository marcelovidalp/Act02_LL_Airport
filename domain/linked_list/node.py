class Node:
    """Nodo para la lista doblemente enlazada"""
    
    def __init__(self, vuelo=None):
        """
        Inicializa un nuevo nodo
        
        Args:
            vuelo: El objeto vuelo asociado al nodo, None para centinelas
        """
        self.vuelo = vuelo      # El vuelo almacenado
        self.next = None        # Referencia al siguiente nodo
        self.prev = None        # Referencia al nodo anterior
        
    def __repr__(self):
        if self.vuelo:
            return f"Node({self.vuelo.numero_vuelo})"
        return "Centinela"
