from src.DataStracture.LinkedList.Node import Node

class LinkedList:
# lista ordinata
    def __init__(self):
         self._root = None

    def get_root(self):
        return self._root

    def set_root(self, root):
        self._root = root

    def insert(self, data):
        new_node = Node(data)
        # usa get_data / set_right per accedere/incapsulare i campi
        if self._root is None or data < self._root.get_data():
            new_node.set_right(self._root)
            self._root = new_node
            return
        current = self._root
        while current.get_right() and current.get_right().get_data() < data:
            current = current.get_right()
        if current.get_right() is None:
            current.set_right(new_node)
        else:
            new_node.set_right(current.get_right())
            current.set_right(new_node)

    def remove(self, data) -> bool:
        if self._root is None:
            return False
        if self._root.get_data() == data:
            # rimozione testa
            self._root = self._root.get_right()
            return True
        current = self._root
        while current.get_right() and current.get_right().get_data() != data:
            current = current.get_right()
        if current.get_right() is None:
            return False
        # salta il nodo da rimuovere
        current.set_right(current.get_right().get_right())
        return True


    def search(self, data) -> Node or None:
        current = self._root
        while current:
            if current.get_data() == data:
                return current
            current = current.get_right()
        return None

    def select(self, k) -> Node or None:
        current = self._root
        count = 1
        while current:
            if count == k:
                return current
            current = current.get_right()
            count += 1
        return None  # k troppo grande

    def rank(self, x) -> int or None:
        current = self._root
        count = 0
        while current and current.get_data() < x:
            count += 1
            current = current.get_right()
        return count

    def to_list(self):
        result = []
        current = self._root
        while current:
            result.append(current.get_data())
            current = current.get_right()
        return result
