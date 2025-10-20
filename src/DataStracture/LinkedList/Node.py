
from src.DataStracture.AstructSracture.ANode import ANode
class Node(ANode) :
    def __init__(self, data):
        self.data = data
        self.next :Node | None = None

    def get_data(self):
        return self.data

    def set(self, data):
        self.data = data

    def get_right(self):
        return self.next


    def set_right(self, node):
        self.next = node