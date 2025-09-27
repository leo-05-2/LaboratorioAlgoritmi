
class Node:
    def __init__(self, key):
        self._left = None
        self._right = None
        self._data = key
        self._father = None

    def get_data(self):
        return self._data


    def set(self, data):
        self._data = data


    def get_left(self):
        return self._left


    def get_right(self):
        return self._right


    def get_father(self):
        return self._father

    def set_left(self, node):
        self._left = node


    def set_right(self, node):
        self._right = node


    def set_father(self, node):
        self._father = node


