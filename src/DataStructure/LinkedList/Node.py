
from src.DataStructure.AstructSracture.ANode import ANode
class Node(ANode) :
    def __init__(self, data):
        super().__init__(data)

    def get_data(self):
        return self._data

    def set(self, data):
        self._data = data

    def get_right(self):
        return self._right


    def set_right(self, node):
        self._right = node

