import numpy as np

class DataGenerator:

    def __init__(self, max_value, length, data_type='random'):
        if length > max_value:
            raise ValueError("La lunghezza non può superare il massimo.")
        self._max_value = max_value
        self._length = length
        self._data_type = data_type

    def start(self):

        if self._data_type == 'random':
            return np.random.choice(self._max_value, self._length, replace=False)
        elif self._data_type == 'sorted':
            # Genera dati ordinati per creare albero degenere (worst case)
            data = np.random.choice(self._max_value, self._length, replace=False)
            return np.sort(data)
        else:
            raise ValueError(f"Tipo di dati non supportato: {self._data_type}")
