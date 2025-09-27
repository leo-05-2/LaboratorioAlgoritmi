

class Node :
    def __init__(self, data):
        self.data = data
        self.next = None

    def get_data(self):
        return self.data

    def set(self, data):
        self.data = data

    def get_next(self):
        return self.next
