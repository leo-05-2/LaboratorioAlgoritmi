from abc import ABC, abstractmethod
from DataStracture.BSTree import Node


class ABSTree(ABC):
    root = None


    @abstractmethod
    def insert(self, key):
        pass

    @abstractmethod
    def search(self, key) -> Node or None:
        pass

    def _min_value_node(self, node):
        current = node
        while current.get_left() is not None:
            current = current.get_left()
        return current

    @abstractmethod
    def remove(self, key) -> bool:
       pass

    def tree_successor(self, node) -> Node or None:
        if node.get_right() is not None:
            return self._min_value_node(node.get_right())
        parent = node.get_father()
        while parent is not None and node == parent.get_right():
            node = parent
            parent = parent.get_father()
        return parent

    def _transplant(self, u, v):
        parent = u.get_father()
        if parent is None:
            self._root = v
        elif u == parent.get_left():
            parent.set_left(v)
        else:
            parent.set_right(v)
        if v is not None:
            v.set_father(parent)

    @abstractmethod
    def in_order(self, node, k, result, count):
        pass

        # funzioni per il confronto

    @abstractmethod
    def select(self, k):
        pass

    @abstractmethod
    def rank(self, x):
        pass



