"""
Test per la struttura dati BSTree.
Si testano: inserimento, ricerca, rimozione, select (k-esimo), rank e tree walk pre-order.
"""
import unittest
from src.DataStracture.BSTree.BStree import BSTree


class TestBSTree(unittest.TestCase):
    def setUp(self):
        self.tree = BSTree()
        for x in [5, 3, 7, 2, 4, 6, 8]:
            self.tree.insert(x)

    def test_pre_order_walk(self):
        result = self.tree.pre_order_walk()
        test_values = [5, 3, 2, 4, 7, 6, 8]
        i =0
        for x in result:
            self.assertEqual(x.get_data(),test_values[i] )
            i+=1

    def test_in_order_walk(self):
        result = self.tree.in_order_walk(self.tree._root, [])
        test_values = [2, 3, 4, 5, 6, 7, 8]
        i =0
        for x in result:
            self.assertEqual(x.get_data(), test_values[i] )
            i+=1

    def test_search(self):
        self.assertIsNotNone(self.tree.search(4))
        self.assertIsNone(self.tree.search(10))

    def test_remove(self):
        self.assertTrue(self.tree.remove(3))
        # Dopo la rimozione, controlliamo il pre-order risultante
        result = self.tree.pre_order_walk()
        test_values = [5, 4, 2, 7, 6, 8]
        i =0
        for x in result:
            self.assertEqual(x.get_data(), test_values[i] )
        self.assertFalse(self.tree.remove(42))

    def test_select(self):
        # Serve in-order per il k-esimo più piccolo
        self.assertEqual(self.tree.select(3).get_data(), 4)

    def test_rank(self):
        self.assertEqual(self.tree.rank(6), 4)  # 2,3,4,5 sono <6

if __name__ == "__main__":
    unittest.main()
