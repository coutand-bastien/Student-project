import sys
import unittest
sys.path.append('../src')

from utils.transform import transform as trans

class TestSort(unittest.TestCase):
    tab1: list = [100, 98, 101]  # dbe
    tab2: list = [97, 98, 99, 100, 101, 102]  # abcdef

    l_tuple: list = [([100, 98, 101], 10), ([120, 99, 10], 85), ([200, 1, 4], 63)]

    def test_list_to_char(self):
        self.assertEqual(trans.list_to_char(self.tab1), "dbe")
        self.assertEqual(trans.list_to_char(self.tab2), "abcdef")

    def test_extract_sub(self):
        self.assertEqual(trans.extract_sub(self.l_tuple, 0), [[100, 98, 101], [120, 99, 10], [200, 1, 4]])
        self.assertEqual(trans.extract_sub(self.l_tuple, 1), [10, 85, 63])