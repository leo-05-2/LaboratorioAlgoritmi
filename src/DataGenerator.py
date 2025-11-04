import numpy as np

class DataGenerator:

    def __init__(self, max_value, length, data_type='random'):
        if length > max_value:
            raise ValueError("La lunghezza non può superare il massimo.")
        self.max_value = max_value
        self.length = length
        self.data_type = data_type

    def start(self):

        if self.data_type == 'random':
            return np.random.choice(self.max_value, self.length, replace=False)
        elif self.data_type == 'sorted':
            # Genera dati ordinati per creare albero degenere (worst case)
            data = np.random.choice(self.max_value, self.length, replace=False)
            return np.sort(data)
        elif self.data_type == 'sorted_desc':
            # Genera dati ordinati decrescenti
            data = np.random.choice(self.max_value, self.length, replace=False)
            return np.sort(data)[::-1]
        elif self.data_type == 'balanced':
            data = np.random.choice(self.max_value, self.length, replace=False)
            sorted_data = np.sort(data)
            return self._balanced_insertion_order(sorted_data)
        else:
            raise ValueError(f"Tipo di dati non supportato: {self.data_type}")

    def _balanced_insertion_order(self, sorted_array):
        if len(sorted_array) == 0:
            return np.array([], dtype=sorted_array.dtype)

        result = []
        queue = [(0, len(sorted_array) - 1)]
        idx = 0

        # BFS over intervals: processa le mediane livello-per-livello
        while idx < len(queue):
            l, r = queue[idx]
            idx += 1
            if l > r:
                continue
            m = (l + r) // 2
            result.append(sorted_array[m])
            # enqueue left e right per essere processati ai livelli successivi
            queue.append((l, m - 1))
            queue.append((m + 1, r))

        return np.array(result, dtype=sorted_array.dtype)
