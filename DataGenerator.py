import numpy as np

class DataGenerator:
    """ Classe per generare dati casuali unici.
    Attributi:
        massimo (int): Il valore massimo per i numeri generati.
        lunghezza (int): La lunghezza della lista di numeri generati.
    """
    def __init__(self, max_value, length):
        if length > max_value:
            raise ValueError("La lunghezza non può superare il massimo.")
        self.max_value = max_value
        self.length = length

    def start(self):
        return np.random.choice(self.max_value, self.length, replace=False)