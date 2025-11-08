import time
import matplotlib.pyplot as plt
from src.DataStracture.LinkedList.LinkedList import LinkedList
from src.DataStracture.BSTree.BStree import BSTree
from src.DataStracture.SBSTree.SBStree import SBStree
from src.DataGenerator import DataGenerator
import numpy as np


class StructureTester:

    def __init__(self, sizes=None, datasets_per_n=6, count=120, calls_per_test=30, warmup_calls=20):
        if sizes is None:
            sizes = np.unique(np.logspace(2, 4, 50, dtype=int))   # da 100 a ~1000, 25 punti
            # size spaziato linearmente tra 100 e 10000 con np e unique
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
        # test per i dati semplici semnza media
        self.agg_select = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.agg_rank = {'LinkedList': [], 'BSTree': [], 'SBStree': []}


    def _measure_on_structure_instance(self, structure, n):

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

        for _ in range(self.count): #test con k diversi per test quindi count esempi per ogni dimensione
            k = int(rng.integers(1, n + 1))

            start = time.perf_counter()
            for __ in range(self.calls_per_test): # con lo stesso k per ridurre rumore
                structure.select(k)
            elapsed_select = (time.perf_counter() - start) / self.calls_per_test
            samples_select.append(elapsed_select)
            x = structure.select(k).get_data()

            start = time.perf_counter()
            for __ in range(self.calls_per_test):
                structure.rank(x)
            elapsed_rank = (time.perf_counter() - start) / self.calls_per_test
            samples_rank.append(elapsed_rank)

        return samples_select, samples_rank

    def run_tests(self, random = True):

        self.select_mean = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.select_std  = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.rank_mean   = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self.rank_std    = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        for n in self.sizes:
            # opzionalmente aggrega più dataset per n (oggi lasciato semplice)
            agg_select = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
            agg_rank   = {'LinkedList': [], 'BSTree': [], 'SBStree': []}

            for ds in range(self.datasets_per_n): # per ridurre rumore

                if not random:
                    # genera dati ordinati per test degenere
                    generator = DataGenerator(n * 2, n, data_type='sorted')
                    data = generator.start()
                else:
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


    def _draw_metric(self, x, structure_names, mean_dict, std_dict, markers, colors, xlabel, ylabel, title, filename,
                     figsize=(10, 5), legend_fontsize=12):
        plt.figure(figsize=figsize)

        for name in structure_names:
            mean  = np.array(mean_dict[name], dtype=float)
            std   = np.array(std_dict[name], dtype=float)
            if mean.size != x.size:
                mean = np.full_like(x, np.nan, dtype=float)
                std = np.full_like(x, np.nan, dtype=float)


            plt.plot(x, mean, label=name, marker=markers[name], color=colors[name], linewidth=2)
            plt.fill_between(x, mean - std, mean + std, color=colors[name], alpha=0.2)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.title(title, fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=legend_fontsize)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    def plot_results(self, flag = False, structure_names = ['LinkedList', 'BSTree', 'SBStree'], random = True):
        markers = {'LinkedList': 'o', 'BSTree': 's', 'SBStree': '^'}
        colors = {'LinkedList': 'tab:blue', 'BSTree': 'tab:orange', 'SBStree': 'tab:green'}
        x = np.array(self.sizes)
        if random:
            test_type = "random"
        else:
            test_type = "degenerate"
        if flag:

            name =''
            for i in structure_names:
                name += f'{i}_'
            name = name[:-1]  # rimuovi l'ultimo underscore


            self._draw_metric(x, structure_names, self.select_mean, self.select_std, markers, colors,
                              'Dimensione struttura', 'Tempo medio select (s)', 'Prestazioni select',
                              f'select_performance_{name}_{test_type}.png')

            self._draw_metric(x, structure_names, self.rank_mean, self.rank_std, markers, colors,
                              'Dimensione struttura', 'Tempo medio rank (s)', 'Prestazioni rank',
                              f'rank_performance_{name}_{test_type}.png')
            return  # Qui gestiamo il caso in cui l'utente passa una selezione di strutture
            # normalizziamo structure_name in lista
        else:
            for name in structure_names:
                if name not in ['LinkedList', 'BSTree', 'SBStree']:
                    raise ValueError(f"Invalid structure name: {name}")
                structure_name = structure_names
                self._draw_metric(x, [name], self.select_mean, self.select_std, markers, colors,
                                  'Dimensione struttura', 'Tempo medio select (s)', f'Prestazioni select: {name}',
                                  f'select_performance_{name}_{test_type}.png')
                self._draw_metric(x, [name], self.rank_mean, self.rank_std, markers, colors,
                                  'Dimensione struttura', 'Tempo medio rank (s)', f'Prestazioni rank: {name}',
                                  f'rank_performance_{name}_{test_type}.png')



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
    

    def run_degenerate_test(self): #todo: albero degenere contro lista, entrambi ordinati
        result_select = {'LinkedList': [], 'BSTree_Degenerate': []}
        result_rank = {'LinkedList': [], 'BSTree_Degenerate': []}

        for n in self.sizes:
            generator = DataGenerator(n * 2, n, data_type='sorted')
            data = generator.start()

            # LinkedList
            ll = LinkedList()
            for v in data:
                ll.insert(v)
            sel_samps, rnk_samps = self._measure_on_structure_instance(ll, n)
            result_select['LinkedList'].append(np.mean(sel_samps))
            result_rank['LinkedList'].append(np.mean(rnk_samps))

            # BSTree con dati ordinati (degenera in lista)
            bst = BSTree()
            for v in data:
                bst.insert(v)
            sel_samps, rnk_samps = self._measure_on_structure_instance(bst, n)
            result_select['BSTree_Degenerate'].append(np.mean(sel_samps))
            result_rank['BSTree_Degenerate'].append(np.mean(rnk_samps))

            print(f'finished degenerate test n={n}')

        return result_select, result_rank

    def run_balanced_test(self): #todo: bilanziato vs random
        result_select = {
            'BSTree_Random': [], 'BSTree_Balanced': [],
            'SBStree_Random': [], 'SBStree_Balanced': []
        }
        result_rank = {
            'BSTree_Random': [], 'BSTree_Balanced': [],
            'SBStree_Random': [], 'SBStree_Balanced': []
        }

        for n in self.sizes:
            # Test Random
            generator_random = DataGenerator(n * 2, n, data_type='random')
            data_random = generator_random.start()

            bst_rand = BSTree()
            for v in data_random:
                bst_rand.insert(v)
            sel_samps, rnk_samps = self._measure_on_structure_instance(bst_rand, n)
            result_select['BSTree_Random'].append(np.mean(sel_samps))
            result_rank['BSTree_Random'].append(np.mean(rnk_samps))

            sbs_rand = SBStree()
            for v in data_random:
                sbs_rand.insert(v)
            sel_samps, rnk_samps = self._measure_on_structure_instance(sbs_rand, n)
            result_select['SBStree_Random'].append(np.mean(sel_samps))
            result_rank['SBStree_Random'].append(np.mean(rnk_samps))

            # Test Balanced
            generator_balanced = DataGenerator(n * 2, n, data_type='balanced')
            data_balanced = generator_balanced.start()

            bst_bal = BSTree()
            for v in data_balanced:
                bst_bal.insert(v)
            sel_samps, rnk_samps = self._measure_on_structure_instance(bst_bal, n)
            result_select['BSTree_Balanced'].append(np.mean(sel_samps))
            result_rank['BSTree_Balanced'].append(np.mean(rnk_samps))

            sbs_bal = SBStree()
            for v in data_balanced:
                sbs_bal.insert(v)
            sel_samps, rnk_samps = self._measure_on_structure_instance(sbs_bal, n)
            result_select['SBStree_Balanced'].append(np.mean(sel_samps))
            result_rank['SBStree_Balanced'].append(np.mean(rnk_samps))

            print(f'finished balanced vs random test n={n}')

        return result_select, result_rank

    #todo:aggiungere albero bilanciato confronto lista


    def plot_degenerate_comparison(self, result_select, result_rank):
        x = np.array(self.sizes)

        # Select plot
        plt.figure(figsize=(10, 5))
        plt.plot(x, result_select['LinkedList'], label='LinkedList',
                 marker='o', color='tab:blue', linewidth=2)
        plt.plot(x, result_select['BSTree_Degenerate'], label='BSTree (Sorted/Degenerate)',
                 marker='s', color='tab:orange', linewidth=2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio select (s)', fontsize=12)
        plt.title('Prestazioni select: LinkedList vs BSTree Degenere', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig('select_degenerate_comparison.png')
        plt.close()

        # Rank plot
        plt.figure(figsize=(10, 5))
        plt.plot(x, result_rank['LinkedList'], label='LinkedList',
                 marker='o', color='tab:blue', linewidth=2)
        plt.plot(x, result_rank['BSTree_Degenerate'], label='BSTree (Sorted/Degenerate)',
                 marker='s', color='tab:orange', linewidth=2)
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio rank (s)', fontsize=12)
        plt.title('Prestazioni rank: LinkedList vs BSTree Degenere', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig('rank_degenerate_comparison.png')
        plt.close()

    def plot_balanced_comparison(self, result_select, result_rank):
        x = np.array(self.sizes)

        # Select plot
        plt.figure(figsize=(12, 5))
        plt.plot(x, result_select['BSTree_Random'], label='BSTree Random',
                 marker='o', color='tab:orange', linewidth=2, linestyle='-')
        plt.plot(x, result_select['BSTree_Balanced'], label='BSTree Balanced',
                 marker='s', color='tab:orange', linewidth=2, linestyle='--')
        plt.plot(x, result_select['SBStree_Random'], label='SBStree Random',
                 marker='^', color='tab:green', linewidth=2, linestyle='-')
        plt.plot(x, result_select['SBStree_Balanced'], label='SBStree Balanced',
                 marker='v', color='tab:green', linewidth=2, linestyle='--')
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio select (s)', fontsize=12)
        plt.title('Prestazioni select: Random vs Balanced Insertion', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=10)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig('select_balanced_comparison.png')
        plt.close()

        # Rank plot
        plt.figure(figsize=(12, 5))
        plt.plot(x, result_rank['BSTree_Random'], label='BSTree Random',
                 marker='o', color='tab:orange', linewidth=2, linestyle='-')
        plt.plot(x, result_rank['BSTree_Balanced'], label='BSTree Balanced',
                 marker='s', color='tab:orange', linewidth=2, linestyle='--')
        plt.plot(x, result_rank['SBStree_Random'], label='SBStree Random',
                 marker='^', color='tab:green', linewidth=2, linestyle='-')
        plt.plot(x, result_rank['SBStree_Balanced'], label='SBStree Balanced',
                 marker='v', color='tab:green', linewidth=2, linestyle='--')
        plt.xlabel('Dimensione struttura', fontsize=12)
        plt.ylabel('Tempo medio rank (s)', fontsize=12)
        plt.title('Prestazioni rank: Random vs Balanced Insertion', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=10)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig('rank_balanced_comparison.png')
        plt.close()


