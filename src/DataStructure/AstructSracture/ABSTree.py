from abc import ABC, abstractmethod
from src.DataStructure.BSTree import Node


class ABSTree(ABC):
    """Classe astratta per alberi di ricerca binari.

    Fornisce un'interfaccia comune e funzioni di utilità per implementazioni
    di alberi (BSTree, AVL, Red-Black, etc.).
    """

    @abstractmethod
    def insert(self, key):
        """Inserisce una chiave nell'albero."""
        pass

    @abstractmethod
    def search(self, key) -> Node or None:
        """Cerca una chiave nell'albero. Ritorna il nodo se trovato, None altrimenti."""
        pass

    @abstractmethod
    def remove(self, key) -> bool:
        """Rimuove una chiave dall'albero. Ritorna True se rimosso, False se non trovato."""
        pass

    @abstractmethod
    def select(self, k):
        """Ritorna il k-esimo nodo più piccolo dell'albero."""
        pass

    @abstractmethod
    def rank(self, x):
        """Ritorna il numero di elementi minori di x nell'albero."""
        pass

    def _min_value_node(self, node):
        """Ritorna il nodo con il valore minimo nel sottoalbero radicato in node."""
        current = node
        while current.get_left() is not None:
            current = current.get_left()
        return current

    def _transplant(self, u, v):
        """Sostituisce il sottoalbero radicato in u con il sottoalbero radicato in v."""
        parent = u.get_father()
        if parent is None:
            self._root = v
        elif u == parent.get_left():
            parent.set_left(v)
        else:
            parent.set_right(v)
        if v is not None:
            v.set_father(parent)

    def in_order_walk(self, node=None, result=None, k=None):
        """Visita inorder dell'albero. Ritorna lista di nodi ordinati.

        Parametri:
        - node: nodo di partenza (None = usa _root)
        - result: lista di accumulazione (None = crea nuova lista)
        - k: numero massimo di elementi (None = tutti)
        """
        # Determina se è la chiamata iniziale (nessun argomento passato)
        is_initial_call = (node is None and result is None)
        if is_initial_call:
            node = getattr(self, '_root', None)
            result = []
        # Se node è None ma result è stato passato, è il caso base della ricorsione
        if node is None:
            return result
        # visita sinistra
        self.in_order_walk(node.get_left(), result)
        result.append(node)
        if k is not None and len(result) == k:
            return result
        # visita destra
        self.in_order_walk(node.get_right(), result)
        return result

    def pre_order_walk(self, node=None, result=None):
        """Visita preorder dell'albero. Ritorna lista di nodi in preorder.

        Parametri:
        - node: nodo di partenza (None = usa _root)
        - result: lista di accumulazione (None = crea nuova lista)
        """
        # Determina se è la chiamata iniziale (nessun argomento passato)
        is_initial_call = (node is None and result is None)
        if is_initial_call:
            node = getattr(self, '_root', None)
            result = []
        if node is None:
            return result
        result.append(node)
        self.pre_order_walk(node.get_left(), result)
        self.pre_order_walk(node.get_right(), result)
        return result

