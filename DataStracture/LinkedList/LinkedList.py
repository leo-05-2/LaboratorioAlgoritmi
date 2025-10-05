from DataStracture.LinkedList.Node import Node

class LinkedList:
# lista ordinata 
    def __init__(self):
         self._root = None
    def insert(self, data):
        new_node = Node(data)
        if self._root is None or data < self._root.data:
            new_node.next = self._root
            self._root = new_node
            return
        current = self._root
        while current.next and current.next.data < data:
            current = current.next
        if current.next is None:
            current.next = new_node
        else:
            new_node.next = current.next
            current.next = new_node

    def remove(self, data) -> bool:
        if self._root is None:
            return False
        if self._root.data == data:
            self._root = self._root.next
            return True
        current = self._root
        while current.next and current.next.data != data:
            current = current.next
        if current.next is None:
            return False
        current.next = current.next.next
        return True


    def search(self, data) -> Node or None:
        current = self._root
        while current:
            if current.data == data:
                return Node
            current = current.next
        return None

    def select(self, k) -> Node or None:
        current = self._root
        count = 1
        while current:
            if count == k:
                return current.data
            current = current.next
            count += 1
        return None  # k troppo grande

    def rank(self, x) -> int or None:
        current = self._root
        count = 0
        while current and current.data < x:
            count += 1
            current = current.next
        return count

    def to_list(self):
        result = []
        current = self._root
        while current:
            result.append(current.data)
            current = current.next
        return result
