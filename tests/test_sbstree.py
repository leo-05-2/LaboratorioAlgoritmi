"""
Test per la struttura dati SBStree.
Si testano: inserimento, ricerca, rimozione, select (k-esimo), rank, tree walk pre-order
e la correttezza del campo size nei nodi.
"""
import unittest
from src.DataStructure.SBSTree.SBStree import SBStree

class TestSBStree(unittest.TestCase):
    def setUp(self):
        self.tree = SBStree()
        for x in [5, 3, 7, 2, 4, 6, 8]:
            self.tree.insert(x)

    def test_pre_order_walk(self):
        result = self.tree.pre_order_walk()
        test_values = [5, 3, 2, 4, 7, 6, 8]
        i = 0
        for x in result:
            self.assertEqual(x.get_data(), test_values[i])
            i += 1

    def test_in_order_walk(self):
        result = self.tree.in_order_walk(self.tree._root, [])
        test_values = [2, 3, 4, 5, 6, 7, 8]
        i = 0
        for x in result:
            self.assertEqual(x.get_data(), test_values[i])
            i += 1

    def test_search(self):
        self.assertIsNotNone(self.tree.search(4))
        self.assertIsNone(self.tree.search(10))

    def test_remove(self):
        self.assertTrue(self.tree.remove(3))
        result = self.tree.pre_order_walk()
        test_values = [5, 4, 2, 7, 6, 8]
        i = 0
        for x in result:
            self.assertEqual(x.get_data(), test_values[i])
            i += 1
        self.assertFalse(self.tree.remove(42))

    def test_select(self):
        self.assertEqual(self.tree.select(3).get_data(), 4)

    def test_rank(self):
        self.assertEqual(self.tree.rank(6), 4)  # 2,3,4,5 sono <6

    def test_size_after_insert(self):
        # Dopo l'inserimento, il root deve avere size 7
        self.assertEqual(self.tree._root.get_size(), 7)
        # Il nodo con valore 3 deve avere size 3 (sottoalbero: 2,3,4)
        node3 = self.tree.search(3)
        self.assertIsNotNone(node3)
        self.assertEqual(node3.get_size(), 3)
        # Il nodo con valore 7 deve avere size 3 (sottoalbero: 6,7,8)
        node7 = self.tree.search(7)
        self.assertIsNotNone(node7)
        self.assertEqual(node7.get_size(), 3)

    def test_size_after_remove(self):
        # Rimuovo un nodo foglia
        self.tree.remove(2)
        self.assertEqual(self.tree._root.get_size(), 6)
        node3 = self.tree.search(3)
        self.assertIsNotNone(node3)
        self.assertEqual(node3.get_size(), 2)
        # Rimuovo un nodo interno
        self.tree.remove(7)
        self.assertEqual(self.tree._root.get_size(), 5)
        self.tree.remove(8)
        node6 = self.tree.search(6)
        self.assertIsNotNone(node6)
        self.assertEqual(node6.get_size(), 1)

    def test_size_after_multiple_operations(self):
        # Inserisco e rimuovo vari nodi e controllo size
        self.tree.insert(1)
        self.assertEqual(self.tree._root.get_size(), 8)
        self.tree.remove(8)
        self.assertEqual(self.tree._root.get_size(), 7)
        self.tree.remove(5)
        self.assertEqual(self.tree._root.get_size(), 6)
        # Non assumiamo che la struttura mantenga la stessa radice (AVL vs BST).
        # Controlliamo invece che l'ordine in-order sia corretto e che le size
        # dei nodi rispecchino il numero di elementi.
        result = self.tree.in_order_walk(self.tree._root, [])
        self.assertEqual([n.get_data() for n in result], [1, 2, 3, 4, 6, 7])
        # La size totale alla radice deve essere 6
        self.assertEqual(self.tree._root.get_size(), 6)

if __name__ == "__main__":
    unittest.main()
