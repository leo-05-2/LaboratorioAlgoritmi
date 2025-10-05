import time
import matplotlib.pyplot as plt
from DataStracture.LinkedList.LinkedList import LinkedList
from DataStracture.BSTree.BStree import BSTree
from DataStracture.SBSTree.SBStree import SBStree
from DataGenerator import DataGenerator
import numpy as np

class StructureTester:
    def __init__(self, sizes=None):
        if sizes is None:
             sizes = np.unique(np.logspace(2, 3.7, 25, dtype=int))   #da 100 a ~5000, 10 punti
#            sizes = [100, 300, 500, 1000, 2000, 3000, 4000, 5000, 7000, 10000]  # dimensioni testate
        self.sizes = sizes
        self.select_times = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.rank_times = {'LinkedList': [], 'BSTree': [], 'SBStree': []}

    def test_structure(self, structure_class, data, k, x):
        count = 10
        result_select_time = []
        result_rank_time = []
        for _ in range(count):  # per riscaldamento
            structure = structure_class()
            for value in data:
                structure.insert(value)
            # Misura tempo select
            start = time.time()
            for _ in range(300):
                structure.select(k)
            select_time = (time.time() - start) / 300 #per la media
            # Misura tempo rank
            start = time.time()
            for _ in range(300):
                structure.rank(x)
            rank_time = (time.time() - start) / 300
            result_select_time.append(select_time)
            result_rank_time.append(rank_time)

        result_select = sum(result_select_time) / count
        result_rank = sum(result_rank_time) / count
        return result_select, result_rank


    def run_tests(self):
        for n in self.sizes:
            generator = DataGenerator(n*2, n)
            data = generator.start()
            k = np.random.randint(1, n+1)  # k casuale tra 1 e n
            x = int(np.median(data))
            # LinkedList
            sel, rnk = self.test_structure(LinkedList, data, k, x)
            self.select_times['LinkedList'].append(sel)
            self.rank_times['LinkedList'].append(rnk)
            # BSTree
            sel, rnk = self.test_structure(BSTree, data, k, x)
            self.select_times['BSTree'].append(sel)
            self.rank_times['BSTree'].append(rnk)
            # SBStree
            sel, rnk = self.test_structure(SBStree, data, k, x)
            self.select_times['SBStree'].append(sel)
            self.rank_times['SBStree'].append(rnk)

    def plot_results(self):
        markers = {'LinkedList': 'o', 'BSTree': 's', 'SBStree': '^'}
        # Grafico tempi select
        plt.figure(figsize=(10,5))
        for name, times in self.select_times.items():
            plt.plot(self.sizes, times, label=name, marker=markers[name], linewidth=2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio select (s)', fontsize=12)
        plt.title('Prestazioni select', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.savefig('select_performance.png')
        plt.close()

        # Grafico tempi rank (stesso stile)
        plt.figure(figsize=(10,5))
        for name, times in self.rank_times.items():
            plt.plot(self.sizes, times, label=name, marker=markers[name], linewidth=2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio rank (s)', fontsize=12)
        plt.title('Prestazioni rank', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.savefig('rank_performance.png')
        plt.close()

    def plot_sbstree_only(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.sizes, self.rank_times['SBStree'], label='SBStree', marker='^', color='green', linewidth=2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio rank (s)', fontsize=12)
        plt.title('Prestazioni rank SBStree', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.savefig('rank_sbstree_only.png')
        plt.close()