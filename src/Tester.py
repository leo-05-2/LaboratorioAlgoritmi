import time
import matplotlib.pyplot as plt
from src.DataStracture.LinkedList.LinkedList import LinkedList
from src.DataStracture.BSTree.BStree import BSTree
from src.DataStracture.SBSTree.SBStree import SBStree
from src.DataGenerator import DataGenerator
import numpy as np


class StructureTester:

    def __init__(self, sizes=None, datasets_per_n=12, count=120, calls_per_test=30, warmup_calls=20):
        if sizes is None:
            sizes = np.unique(np.logspace(2, 4, 54, dtype=int))   # da 100 a ~1000, 25 punti
        self.sizes = sizes
        self.datasets_per_n = datasets_per_n  # se >1 si possono aggregare più dataset per ogni n
        self.count = count                      # numero di k scelti per n (campioni per n)
        self.calls_per_test = calls_per_test    # numero di chiamate ripetute per misurare una singola prova
        self.warmup_calls = warmup_calls


        # risultati: medi e std per ogni struttura e per ogni n (in ordine di self.sizes)
        self.select_mean = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.select_std  = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.rank_mean   = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.rank_std    = {'LinkedList': [], 'BSTree': [], 'SBStree': []}

    def _measure_on_structure_instance(self, structure, n):
        """
        structure: istanza già popolata
        esegue warmup, poi per self.count volte sceglie un k casuale e misura avg time di select e rank
        restituisce due liste: samples_select (len = self.count), samples_rank
        """
        rng = np.random.default_rng()
        # warm-up
        for _ in range(self.warmup_calls):
            k = int(rng.integers(1, n + 1))
            try:
                structure.select(k)
                structure.rank(k)
            except Exception:
                pass  # ignora errori in warmup

        samples_select = []
        samples_rank = []

        for _ in range(self.count): #test con k diversi per test
            k = int(rng.integers(1, n + 1))
            # measure select
            start = time.perf_counter()
            for __ in range(self.calls_per_test): # con lo stesso k per ridurre rumore
                structure.select(k)
            elapsed_select = (time.perf_counter() - start) / self.calls_per_test
            samples_select.append(elapsed_select)

            # measure rank
            start = time.perf_counter()
            for __ in range(self.calls_per_test):
                structure.rank(k)
            elapsed_rank = (time.perf_counter() - start) / self.calls_per_test
            samples_rank.append(elapsed_rank)

        return samples_select, samples_rank

    def run_tests(self):

        for n in self.sizes:
            # opzionalmente aggrega più dataset per n (oggi lasciato semplice)
            agg_select = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
            agg_rank   = {'LinkedList': [], 'BSTree': [], 'SBStree': []}

            for ds in range(self.datasets_per_n): # per ridurre rumore
                generator = DataGenerator(n * 2, n)
                data = generator.start()

                # LinkedList
                ll = LinkedList()
                for v in data:
                    ll.insert(v)
                sel_samps, rnk_samps = self._measure_on_structure_instance(ll, n)
                agg_select['LinkedList'].extend(sel_samps)
                agg_rank['LinkedList'].extend(rnk_samps)

                # BSTree
                bst = BSTree()
                for v in data:
                    bst.insert(v)
                sel_samps, rnk_samps = self._measure_on_structure_instance(bst, n)
                agg_select['BSTree'].extend(sel_samps)
                agg_rank['BSTree'].extend(rnk_samps)

                # SBStree
                sbs = SBStree()
                for v in data:
                    sbs.insert(v)
                sel_samps, rnk_samps = self._measure_on_structure_instance(sbs, n)
                agg_select['SBStree'].extend(sel_samps)
                agg_rank['SBStree'].extend(rnk_samps)

            # calcola media e std (su tutti i sample aggregati per n)
            for name in ['LinkedList', 'BSTree', 'SBStree']:
                sel_arr = np.array(agg_select[name], dtype=float)
                rnk_arr = np.array(agg_rank[name], dtype=float)

                if sel_arr.size == 0:
                    sel_mean, sel_std = 0.0, 0.0
                else:
                    sel_mean, sel_std = float(np.mean(sel_arr)), float(np.std(sel_arr, ddof=0))

                if rnk_arr.size == 0:
                    rnk_mean, rnk_std = 0.0, 0.0
                else:
                    rnk_mean, rnk_std = float(np.mean(rnk_arr)), float(np.std(rnk_arr, ddof=0))

                self.select_mean[name].append(sel_mean)
                self.select_std[name].append(sel_std)
                self.rank_mean[name].append(rnk_mean)
                self.rank_std[name].append(rnk_std)

            print(f'finished n={n} (datasets_per_n={self.datasets_per_n})')

    def plot_results(self):
        markers = {'LinkedList': 'o', 'BSTree': 's', 'SBStree': '^'}
        colors = {'LinkedList': 'tab:blue', 'BSTree': 'tab:orange', 'SBStree': 'tab:green'}
        x = np.array(self.sizes)

        # select plot
        plt.figure(figsize=(10, 5))
        for name in ['LinkedList', 'BSTree', 'SBStree']:
            mean = np.array(self.select_mean[name], dtype=float)
            std  = np.array(self.select_std[name], dtype=float)
            # sicurezza: se la lunghezza non coincide, riempi con nan per mantenere l'asse
            if mean.size != x.size:
                mean = np.full_like(x, np.nan, dtype=float)
                std = np.full_like(x, np.nan, dtype=float)
            plt.plot(x, mean, label=name, marker=markers[name], color=colors[name], linewidth=2)
            plt.fill_between(x, mean - std, mean + std, color=colors[name], alpha=0.2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio select (s)', fontsize=12)
        plt.title('Prestazioni select', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig('select_performance.png')
        plt.close()

        # rank plot
        plt.figure(figsize=(10, 5))
        for name in ['LinkedList', 'BSTree', 'SBStree']:
            mean = np.array(self.rank_mean[name], dtype=float)
            std  = np.array(self.rank_std[name], dtype=float)
            if mean.size != x.size:
                mean = np.full_like(x, np.nan, dtype=float)
                std = np.full_like(x, np.nan, dtype=float)
            plt.plot(x, mean, label=name, marker=markers[name], color=colors[name], linewidth=2)
            plt.fill_between(x, mean - std, mean + std, color=colors[name], alpha=0.2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio rank (s)', fontsize=12)
        plt.title('Prestazioni rank', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig('rank_performance.png')
        plt.close()

    def plot_sbstree_only(self):
        x = np.array(self.sizes)
        plt.figure(figsize=(10, 5))
        mean = np.array(self.rank_mean['SBStree'], dtype=float)
        std  = np.array(self.rank_std['SBStree'], dtype=float)
        if mean.size != x.size:
            mean = np.full_like(x, np.nan, dtype=float)
            std = np.full_like(x, np.nan, dtype=float)
        plt.plot(x, mean, label='SBStree', marker='^', color='green', linewidth=2)
        plt.fill_between(x, mean - std, mean + std, color='green', alpha=0.2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio rank (s)', fontsize=12)
        plt.title('Prestazioni rank SBStree', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig('rank_sbstree_only.png')
        plt.close()