from DataStracture.BSTree.Node import Node
from DataStracture.AstructSracture.ABSTree import ABSTree


class BSTree(ABSTree):
    def __init__(self):
        self._root = None

    def get_root(self):
        return self._root

    def set_root(self, root):
        self._root = root

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

    def in_order(self, node, k, result,count):
        if node is None or result[0] is not None:
            return
        self.in_order(node.get_left(), k, result, count)
        if result[0] is None:
              count[0] += 1
              if count[0] == k:
                result[0] = node.get_data()
                return
        self.in_order(node.get_right(), k, result, count)

    def _subtree_size(self, node):
        if node is None:
            return 0
        return 1 + self._subtree_size(node.get_left()) + self._subtree_size(node.get_right())


# funzioni per il confronto
    def select(self, k):

        result = [None]
        count = [0]
        self.in_order(self._root,k,result,count)
        return result

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
#insert e delete


    def pre_order_walk(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self._root
            result.append(node)
            return result
        if node:
            result.append(node.get_data())
            self.pre_order_walk(node.get_left(), result)
            self.pre_order_walk(node.get_right(), result)
        return result
