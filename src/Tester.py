import time
import matplotlib.pyplot as plt
from src.DataStracture.LinkedList.LinkedList import LinkedList
from src.DataStracture.BSTree.BStree import BSTree
from src.DataStracture.SBSTree.SBStree import SBStree
from src.DataGenerator import DataGenerator
import numpy as np


class StructureTester:

    def __init__(self, sizes=None):
        if sizes is None:
             sizes = np.unique(np.logspace(2, 3, 25, dtype=int))   #da 100 a ~5000, 25 punti
        self.sizes = sizes
        self.select_times = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.rank_times = {'LinkedList': [], 'BSTree': [], 'SBStree': []}

    def test_structure(self, structure_class, data , n):
        count = 50  # aumentato per maggiore robustezza
        calls_per_test = 300  # aumentato per maggiore precisione
        result_select_time = []
        result_rank_time = []
        structure = structure_class()
        for value in data:
            structure.insert(value)
        for _ in range(count):
            k = np.random.randint(1, n + 1)  # k casuale tra 1 e n


            # Misura tempo select
            start = time.time()
            for _ in range(calls_per_test):
                structure.select(k)
            select_time = (time.time() - start) / calls_per_test
            # Misura tempo rank
            start = time.time()
            for _ in range(calls_per_test):
                structure.rank(k)
            rank_time = (time.time() - start) / calls_per_test
            result_select_time.append(select_time)
            result_rank_time.append(rank_time)


        result_select = sum(result_select_time) / count
        result_rank = sum(result_rank_time) / count
        return result_select, result_rank



    def run_tests(self):
        for n in self.sizes:
            generator = DataGenerator(n*2, n)
            data = generator.start()
            # k = np.random.randint(1, n+1)  # k casuale tra 1 e n
            # x = int(np.median(data))
            # LinkedList
            sel, rnk = self.test_structure(LinkedList, data,n)
            self.select_times['LinkedList'].append(sel)
            self.rank_times['LinkedList'].append(rnk)
            print( 'linked list tested')
            # BSTree
            sel, rnk = self.test_structure(BSTree, data, n)
            self.select_times['BSTree'].append(sel)
            self.rank_times['BSTree'].append(rnk)
            print('bs tested')
            # SBStree
            sel, rnk = self.test_structure(SBStree, data, n)
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