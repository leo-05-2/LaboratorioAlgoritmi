import time
import matplotlib.pyplot as plt
from src.DataStructure.LinkedList.LinkedList import LinkedList
from src.DataStructure.BSTree.BStree import BSTree
from src.DataStructure.SBSTree.SBStree import SBStree
from src.DataGenerator import DataGenerator
import numpy as np
import os
os.makedirs('png', exist_ok=True)

class StructureTester:

    def __init__(self, datasets_per_n=10, count=120, calls_per_test=30, warmup_calls=20):

        sizes = np.unique(np.logspace(0, 4, 50, dtype=int))   # da 100 a ~1000, 25 punti
            # size spaziato linearmente tra 100 e 10000 con np e unique
        self._sizes = sizes
        self._datasets_per_n = datasets_per_n  # se >1 si possono aggregare più dataset per ogni n
        self._count = count                      # numero di k scelti per n (campioni per n)
        self._calls_per_test = calls_per_test    # numero di chiamate ripetute per misurare una singola prova
        self._warmup_calls = warmup_calls


        # risultati: medi e std per ogni struttura e per ogni n (in ordine di self.sizes)
        self._select_mean = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self._select_std  = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self._rank_mean   = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self._rank_std    = {'LinkedList': [], 'BSTree': [], 'SBStree': []}



    def _measure_on_structure_instance(self, structure, n):

        rng = np.random.default_rng()
        # warm-up
        for _ in range(self._warmup_calls):
            k = int(rng.integers(1, n + 1))
            try:
                structure.select(k)
                structure.rank(k)
            except Exception:
                pass  # ignora errori in warmup

        samples_select = []
        samples_rank = []

        for _ in range(self._count): #test con k diversi per test quindi count esempi per ogni dimensione
            k = int(rng.integers(1, n + 1))

            start = time.perf_counter()
            for __ in range(self._calls_per_test): # con lo stesso k per ridurre rumore
                structure.select(k)
            elapsed_select = (time.perf_counter() - start) / self._calls_per_test
            samples_select.append(elapsed_select)
            x = structure.select(k).get_data()

            start = time.perf_counter()
            for __ in range(self._calls_per_test):
                structure.rank(x)
            elapsed_rank = (time.perf_counter() - start) / self._calls_per_test
            samples_rank.append(elapsed_rank)

        return samples_select, samples_rank

    def run_tests(self, random = True):

        self._select_mean = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self._select_std  = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self._rank_mean   = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        self._rank_std    = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
        for n in self._sizes:
            # opzionalmente aggrega più dataset per n (oggi lasciato semplice)
            agg_select = {'LinkedList': [], 'BSTree': [], 'SBStree': []}
            agg_rank   = {'LinkedList': [], 'BSTree': [], 'SBStree': []}

            for ds in range(self._datasets_per_n): # per ridurre rumore

                if random == False:
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

                self._select_mean[name].append(sel_mean)
                self._select_std[name].append(sel_std)
                self._rank_mean[name].append(rnk_mean)
                self._rank_std[name].append(rnk_std)

            print(f'finished n={n} (datasets_per_n={self._datasets_per_n})')
        type_label = "sorted" if random == False else "random"
        self._save_to_latex(type_label)

        print(f"Test {type_label} completati.\n")


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
        x = np.array(self._sizes)
        if random:
            test_type = "random"
        else:
            test_type = "sorted"
        if flag:
            name =''
            for i in structure_names:
                name += f'{i}_'
            name = name[:-1]  # rimuove l'ultimo underscore
            self._draw_metric(x, structure_names, self._select_mean, self._select_std, markers, colors,
                              'Dimensione struttura', 'Tempo medio select (s)', 'Prestazioni select',
                              f'png/select_performance_{name}_{test_type}.png')

            self._draw_metric(x, structure_names, self._rank_mean, self._rank_std, markers, colors,
                              'Dimensione struttura', 'Tempo medio rank (s)', 'Prestazioni rank',
                              f'png/rank_performance_{name}_{test_type}.png')
            return
        else:
            for name in structure_names:
                if name not in ['LinkedList', 'BSTree', 'SBStree']:
                    raise ValueError(f"Invalid structure name: {name}")
                structure_name = structure_names
                self._draw_metric(x, [name], self._select_mean, self._select_std, markers, colors,
                                  'Dimensione struttura', 'Tempo medio select (s)', f'Prestazioni select: {name}',
                                  f'png/select_performance_{name}_{test_type}.png')
                self._draw_metric(x, [name], self._rank_mean, self._rank_std, markers, colors,
                                  'Dimensione struttura', 'Tempo medio rank (s)', f'Prestazioni rank: {name}',
                                  f'png/rank_performance_{name}_{test_type}.png')

    def _save_to_latex(self, test_type):
        filename = f"plt/tabella_risultati_{test_type}.tex"
        print(f"   -> Generazione tabella LaTeX (Sync Indici) in {filename}...")

        structures = list(self._select_mean.keys())
        SIG_FIGS = 3

        try:
            # Assicuriamoci che la directory esista prima di scrivere il file
            dirpath = os.path.dirname(filename)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)
            with open(filename, 'w') as f:
                # --- Intestazione Tabella ---
                f.write("\\begin{table}[h!]\n")
                f.write("\\centering\n")
                f.write("\\resizebox{\\textwidth}{!}{%\n")

                cols = "|c" + "|c" * (len(structures) * 2) + "|"
                f.write(f"\\begin{{tabular}}{{{cols}}}\n")
                f.write("\\hline\n")

                # Header 1: Nomi Strutture
                header1 = "\\multirow{2}{*}{\\textbf{N}}"
                for struct in structures:
                    header1 += f" & \\multicolumn{{2}}{{c|}}{{\\textbf{{{struct}}}}}"
                f.write(header1 + " \\\\\n")

                # Header 2: Select / Rank
                header2 = ""
                for _ in structures:
                    header2 += " & Select (s) & Rank (s)"
                f.write(header2 + " \\\\\n")
                f.write("\\hline\n")

                # --- LOGICA SEMPLIFICATA BASATA SUGLI ARRAY ---

                # 1. Troviamo quanti dati validi abbiamo.
                # Prendiamo la lunghezza della prima struttura come riferimento.
                first_struct = structures[0]
                data_count = len(self._select_mean[first_struct])

                # Se non ci sono dati, usciamo
                if data_count == 0:
                    f.write("\\multicolumn{" + str(1 + len(structures) * 2) + "}{|c|}{Nessun dato disponibile} \\\\\n")
                else:
                    # 2. Decidiamo quali indici stampare (Campionamento)
                    # Vogliamo circa 15 righe al massimo per non intasare la pagina
                    step = max(1, data_count // 15)

                    # Generiamo la lista degli indici: 0, step, 2*step...
                    indices = list(range(0, data_count, step))

                    # 3. Assicuriamoci che l'ULTIMO indice dell'array sia presente
                    # (Quello che contiene il N massimo testato, es. 10.000)
                    last_real_index = data_count - 1
                    if indices[-1] != last_real_index:
                        indices.append(last_real_index)

                    # 4. Iteriamo solo su questi indici sincronizzati
                    for i in indices:
                        # Prendo la dimensione N corrispondente a questo indice
                        n = self._sizes[i]
                        row = f"{n}"

                        for struct in structures:
                            # Sicurezza: controlliamo che anche le altre strutture abbiano dati a questo indice
                            if i < len(self._select_mean[struct]):
                                val_select = self._select_mean[struct][i]
                                val_rank = self._rank_mean[struct][i]

                                s_val = self._format_smart_latex(val_select, SIG_FIGS)
                                r_val = self._format_smart_latex(val_rank, SIG_FIGS)
                                row += f" & {s_val} & {r_val}"
                            else:
                                # Se una struttura ha meno dati delle altre (errore raro ma possibile)
                                row += " & - & -"

                        f.write(row + " \\\\\n")
                        f.write("\\hline\n")

                # Chiusura
                f.write("\\end{tabular}\n")
                f.write("}\n")
                f.write(f"\\caption{{Tempi medi per dataset {test_type} (Cifre sign.: {SIG_FIGS}).}}\n")
                f.write(f"\\label{{tab:{test_type}}}\n")
                f.write("\\end{table}\n")

        except IOError as e:
            print(f"Errore salvataggio LaTeX: {e}")

    def _format_smart_latex(self, val, sig_figs=3):
        """
        Formatta il numero usando un numero fisso di cifre significative (sig_figs).
        - Se il numero è 'normale' (es. 0.0123), usa la notazione decimale.
        - Se è molto piccolo o molto grande, passa automaticamente alla notazione scientifica.
        - Converte la notazione scientifica 'e' in LaTeX ($ \\times 10^{x} $).
        """
        if val is None or np.isnan(val):
            return "-"
        if val == 0:
            return "0"

        # Usa il formato 'g' che gestisce automaticamente le cifre significative
        formatted_str = f"{val:.{sig_figs}e}"

        # Se Python usa la notazione scientifica (c'è una 'e'), convertiamola in LaTeX
        if 'e' in formatted_str:
            base, exponent = formatted_str.split('e')
            exponent = int(exponent)  # Rimuove zeri extra (es. -05 -> -5)
            return f"${base} \\times 10^{{{exponent}}}$"
        else:
            # Altrimenti è un numero decimale normale
            return f"${formatted_str}$"
