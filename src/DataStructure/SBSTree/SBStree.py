from src.DataStructure.AstructSracture.ABSTree import ABSTree
from src.DataStructure.SBSTree.Node import Node


class SBStree(ABSTree):
    def __init__(self):
        self._root = None

    def get_root(self):
        return self._root

    def set_root(self, root):
        self._root = root

    def left_rotate(self, x):
        y = x.get_right()
        x.set_right(y.get_left())
        if y.get_left() is not None:
            y.get_left().set_father(x)
        y.set_father(x.get_father())
        if x.get_father() is None:
            self._root = y
        elif x is x.get_father().get_left():
            x.get_father().set_left(y)
        else:
            x.get_father().set_right(y)
        y.set_left(x)
        x.set_father(y)
        x.update_height()
        y.update_height()
        x.set_size(1 + (x.get_left().get_size() if x.get_left() is not None else 0) + (x.get_right().get_size() if x.get_right() is not None else 0))
        y.set_size(1 + (y.get_left().get_size() if y.get_left() is not None else 0) + (y.get_right().get_size() if y.get_right() is not None else 0))

    def right_rotate(self, y):
        x = y.get_left()
        y.set_left(x.get_right())
        if x.get_right() is not None:
            x.get_right().set_father(y)
        x.set_father(y.get_father())
        if y.get_father() is None:
            self._root = x
        elif y is y.get_father().get_right():
            y.get_father().set_right(x)
        else:
            y.get_father().set_left(x)
        x.set_right(y)
        y.set_father(x)
        y.update_height()
        x.update_height()
        y.set_size(1 + (y.get_left().get_size() if y.get_left() is not None else 0) + (y.get_right().get_size() if y.get_right() is not None else 0))
        x.set_size(1 + (x.get_left().get_size() if x.get_left() is not None else 0) + (x.get_right().get_size() if x.get_right() is not None else 0))

    def _rebalance(self, node):
        current = node
        while current is not None:
            left = current.get_left()
            right = current.get_right()
            old_h = current.get_height()
            old_size = current.get_size()

            left_h = left.get_height() if left is not None else 0
            right_h = right.get_height() if right is not None else 0
            balance = left_h - right_h

            # esegue rotazioni se necessario
            rotated = False
            if balance > 1:
                if left is not None and left.get_balance() < 0:
                    self.left_rotate(left)
                self.right_rotate(current)

                current = current.get_father()
                rotated = True
            elif balance < -1:
                if right is not None and right.get_balance() > 0:
                    self.right_rotate(right)
                self.left_rotate(current)

                current = current.get_father()
                rotated = True

            # Se non c'è stata rotazione, si aggiorna current normalmente
            if not rotated:

                left = current.get_left()
                right = current.get_right()

                left_h = left.get_height() if left is not None else 0
                right_h = right.get_height() if right is not None else 0
                new_h = 1 + (left_h if left_h > right_h else right_h)
                current.set_height(new_h)
                left_size = left.get_size() if left is not None else 0
                right_size = right.get_size() if right is not None else 0
                current.set_size(1 + left_size + right_size)

                # se height e size non sono cambiate, non servono aggiornamenti superiori
                new_size = current.get_size()
                if new_h == old_h and new_size == old_size:
                    break


            current = current.get_father()

    def insert(self, key):
        node = Node(key)
        if self._root is None:
            self._root = node
            return
        current = self._root
        parent = None
        while current is not None:
            parent = current
            if key < current.get_data():
                current = current.get_left()
            elif key > current.get_data():
                current = current.get_right()
            else:

                return
        node.set_father(parent)
        if key < parent.get_data():
            parent.set_left(node)
        else:
            parent.set_right(node)
        self._rebalance(parent)

    def search(self, key) -> Node or None:
        current = self._root
        while current is not None:
            if current.get_data() == key:
                return current
            elif key < current.get_data():
                current = current.get_left()
            else:
                current = current.get_right()
        return None

    def _update_size_upwards(self, node):
        while node is not None:
            left_size = node.get_left().get_size() if node.get_left() is not None else 0
            right_size = node.get_right().get_size() if node.get_right() is not None else 0
            node.set_size(1 + left_size + right_size)
            node.update_height()
            node = node.get_father()

    def remove(self, key) -> bool:
        node = self.search(key)
        if node is None:
            return False
        self._delete_node(node)
        return True

    def _delete_node(self, z):
        if z.get_left() is None:
            x_parent = z.get_father()
            self._transplant(z, z.get_right())
            self._update_size_upwards(x_parent)
            self._rebalance(x_parent)
        elif z.get_right() is None:
            x_parent = z.get_father()
            self._transplant(z, z.get_left())
            self._update_size_upwards(x_parent)
            self._rebalance(x_parent)
        else:
            y = self._min_value_node(z.get_right())
            y_original_parent = y.get_father()
            if y.get_father() is not z:

                self._transplant(y, y.get_right())

                y.set_father(None)
                self._update_size_upwards(y_original_parent)

                y.set_right(z.get_right())
                if y.get_right() is not None:
                    y.get_right().set_father(y)
            self._transplant(z, y)
            y.set_left(z.get_left())
            if y.get_left() is not None:
                y.get_left().set_father(y)
            self._update_size_upwards(y)
            self._rebalance(y)

    def select(self, k):
        return self._select(self._root, k)

    def _select(self, node, k):
        if node is None:
            return None
        left_size = node.get_left().get_size() if node.get_left() is not None else 0
        if k == left_size + 1:
            return node
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
            left_size = node.get_left().get_size() if node.get_left() is not None else 0
            return 1 + left_size + self._rank(node.get_right(), x)
        else:
            left_size = node.get_left().get_size() if node.get_left() is not None else 0
            return left_size
