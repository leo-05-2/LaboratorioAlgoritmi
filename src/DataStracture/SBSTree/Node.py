from ..AstructSracture.ANode import ANode
class Node(ANode):
    def __init__(self, key):
        # usa il costruttore astratto per inizializzare _data e _right
        super().__init__(key)
        # attributi specifici dei nodi di alberi bilanciati
        self._left = None
        self._father = None
        self._size = 1
        self._height = 1

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


    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    # Height / balance helpers per AVL
    def get_height(self):
        return self._height

    def set_height(self, h):
        self._height = h

    def update_height(self):
        lh = self._left._height if (self._left is not None) else 0
        rh = self._right._height if (self._right is not None) else 0
        self._height = 1 + (lh if lh > rh else rh)

    def get_balance(self):
        lh = self._left._height if (self._left is not None) else 0
        rh = self._right._height if (self._right is not None) else 0
        return lh - rh
