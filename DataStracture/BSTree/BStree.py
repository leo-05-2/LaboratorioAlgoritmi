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
        if node.get_left() is None and node.get_right() is None:
            parent = node.get_father()
            if parent is None:
                self._root = None
            elif parent.get_left() == node:
                parent.set_left(None)
            else:
                parent.set_right(None)
            return
        if node.get_left() is None or node.get_right() is None:
            if node.get_left():
                child = node.get_left()
            else:
                child = node.get_right()
            parent = node.get_father()
            if parent is None:
                self._root = child
            elif parent.get_left() == node:
                parent.set_left(child)
            else:
                parent.set_right(child)
            if child:
                child.set_father(parent)
            return


        successor = self.tree_successor(node)
        node.set_data(successor.get_data())
        self._remove(successor)








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