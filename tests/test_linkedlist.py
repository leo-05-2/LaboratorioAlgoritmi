import unittest
from DataStracture.LinkedList.LinkedList import LinkedList

class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.list = LinkedList()
        for x in [5, 3, 7, 2, 4, 6, 8]:
            self.list.insert(x)

    def test_insert_and_order(self):
        # Verifica che gli elementi siano inseriti in ordine
        current = self.list._root
        expected_values = [2, 3, 4, 5, 6, 7, 8]
        for value in expected_values:
            self.assertIsNotNone(current)
            self.assertEqual(current.data, value)
            current = current.next
        self.assertIsNone(current)  # La lista deve terminare qui

    def test_search(self):
        self.assertIsNotNone(self.list.search(4))
        self.assertIsNone(self.list.search(10))

    def test_remove(self):
        self.assertTrue(self.list.remove(3))
        # Dopo la rimozione, controlliamo l'ordine risultante
        current = self.list._root
        expected_values = [2, 4, 5, 6, 7, 8]
        for value in expected_values:
            self.assertIsNotNone(current)
            self.assertEqual(current.data, value)
            current = current.next
        self.assertIsNone(current)  # La lista deve terminare qui
        self.assertFalse(self.list.remove(42))

    def test_select (self):
        self.assertEqual(self.list.select(3), 4)
        self.assertIsNone(self.list.select(10))  # k troppo grande

    def test_rank(self):
        self.assertEqual(self.list.rank(6), 4)  # 2,3,4,5 sono <6
        self.assertEqual(self.list.rank(1), 0)  # Nessun elemento <1
        self.assertEqual(self.list.rank(9), 7)  # Tutti gli elementi <9

    def test_insert(self):
        # controlla che dopo insert la lista sia ordinata

        current = self.list._root
        expected_values = [2, 3, 4, 5, 6, 7, 8]
        for value in expected_values:
            self.assertIsNotNone(current)
            self.assertEqual(current.data, value)
            current = current.next
        self.assertIsNone(current)

    def test_remove_head(self):
        # rimuove la testa della lista
        self.assertTrue(self.list.remove(2))
        current = self.list._root
        expected_values = [3, 4, 5, 6, 7, 8]
        for value in expected_values:
            self.assertIsNotNone(current)
            self.assertEqual(current.data, value)
            current = current.next
        self.assertIsNone(current)