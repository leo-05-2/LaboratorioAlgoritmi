from typing import Optional

from src.DataStructure.BSTree.Node import Node
from src.DataStructure.AstructSracture.ABSTree import ABSTree


class BSTree(ABSTree):
    def __init__(self):
        self._root = None

    def get_root(self):
        return self._root

    def set_root(self, root):
        self._root = root

    def insert(self, key):
        new_node = Node(key)
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

    def search(self, key) -> Node | None:
        current = self._root
        while current:
            if current.get_data() == key:
                return current
            elif key < current.get_data():
                current = current.get_left()
            else:
                current = current.get_right()
        return None

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

    def _subtree_size(self, node):
        if node is None:
            return 0
        return 1 + self._subtree_size(node.get_left()) + self._subtree_size(node.get_right())

# funzioni per il confronto
    def select(self, k):

        if k is None or k <= 0 or self._root is None:
            return None

        stack = []
        current :Optional[Node] = self._root
        count = 0

        while stack or current:
            while current:
                stack.append(current)
                current = current.get_left()
            current = stack.pop()
            count += 1
            if count == k:
                return current
            current = current.get_right()

        return None

    def rank(self, x):
        current = self._root
        rank = 0
        while current:
            if x > current.get_data():
                left_size = self._subtree_size(current.get_left())
                rank += 1 + left_size
                current = current.get_right()
            else:
                current = current.get_left()
        return rank