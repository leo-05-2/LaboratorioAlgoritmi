from Node import *
from DataStracture.AstructSracture.ABSTree import ABSTree

class SBStree(ABSTree):
    def __init__(self):
        self._root = None

    def insert(self, key):
        self._root = self._insert(self._root, key)


    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.get_data():
            node.set_left(self._insert(node.get_left(), key))
            node.get_left().set_father(node)
        else:
            node.set_right(self._insert(node.get_right(), key))
            node.get_right().set_father(node)
        node.set_size(1 + (node.get_left().get_size() if node.get_left() else 0) +
                         (node.get_right().get_size() if node.get_right() else 0))
        return node

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



    def _update_size_upwards(self, node):
        while node:
            left_size = node.get_left().get_size() if node.get_left() else 0
            right_size = node.get_right().get_size() if node.get_right() else 0
            node.set_size(1 + left_size + right_size)
            node = node.get_father()

    def remove(self, key) -> bool:
        node = self.search(key)
        if node is None:
            return False
        parent = node.get_father()
        self._remove(node)
        self._update_size_upwards(parent)
        return True

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
            self._update_size_upwards(successor)

    def select(self, k):
        return self._select(self._root, k)


    def _select(self, node, k):
        if node is None:
            return None
        left_size = node.get_left().get_size() if node.get_left() else 0
        if k == left_size + 1:
            return node.get_data()
        elif k <= left_size:
            return self._select(node.get_left(), k)
        else:
            return self._select(node.get_right(), k - left_size - 1)

    def rank(self, x):
        return self._rank(self._root, x)


    def _rank(self, node, x):
        if node is None:
            return 0
        if x < node.get_data():
            return self._rank(node.get_left(), x)
        elif x > node.get_data():
            left_size = node.get_left().get_size() if node.get_left() else 0
            return 1 + left_size + self._rank(node.get_right(), x)
        else:
            left_size = node.get_left().get_size() if node.get_left() else 0
            return left_size


    def pre_order_walk(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self._root
        if node:
            result.append(node.get_data())
            self.pre_order_walk(node.get_left(), result)
            self.pre_order_walk(node.get_right(), result)
        return result
