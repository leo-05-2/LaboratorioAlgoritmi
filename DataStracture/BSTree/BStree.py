from Node import *

class BSTree:
    def __init__(self):
        self._root = None

    def insert(self, key):
        new_node = Node(key)  #rimane da gestire il caso in cui un valore sia uguale al nuovo dato
        if self._root is None:
            self._root = new_node
            return
        current = self._root
        while True:
            if key < current.get_data():
                if current.get_left() is None:
                    current.set_left(new_node)
                    new_node.set_father(current)
                    return
                else:
                    current = current.get_left()
            else:
                if current.get_right() is None:
                    current.set_right(new_node)
                    new_node.set_father(current)
                    return
                else:
                    current = current.get_right()

    def search(self, key) -> Node or None:
        current = self._root
        while current:
            if current.get_data() == key:
                return current
            elif key < current.get_data():
                current = current.get_left()
            else:
                current = current.get_right()
        return None

    def _min_value_node(self, node):
        current = node
        while current.get_left() is not None:
            current = current.get_left()
        return current

    def _remove(self, node):
        if node.get_left() is None:
            self._transplant(node, node.get_right())
        elif node.get_right() is None:
            self._transplant(node, node.get_left())
        else:
            successor = self._min_value_node(node.get_right())
            if successor.get_father() != node:
                self._transplant(successor, successor.get_right())
                successor.set_right(node.get_right())
                successor.get_right().set_father(successor)
            self._transplant(node, successor)
            successor.set_left(node.get_left())
            successor.get_left().set_father(successor)

    def remove(self, key) -> bool:
        node = self.search(key)
        if node is None:
            return False
        self._remove(node)
        return True

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

