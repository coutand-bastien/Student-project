import sys
import unittest
sys.path.append('../src')

from utils.sort import sort as sort

class TestSort(unittest.TestCase):
    tab1: list = [3, 5, 5, 12, 85, -2, -45, 7]
    tab2: list = [-458, 0, 85, 69, 159, 74, 58]

    def test_fusion_sort_decreasing(self):
        self.assertEqual(sort.fusion_sort_decreasing(self.tab1), [85, 12, 7, 5, 5, 3, -2, -45])
        self.assertEqual(sort.fusion_sort_decreasing(self.tab2), [159, 85, 74, 69, 58, 0, -458])

    def test_fusion_sort_growing(self):
        self.assertEqual(sort.fusion_sort_growing(self.tab1), [-45, -2, 3, 5, 5, 7, 12, 85])
        self.assertEqual(sort.fusion_sort_growing(self.tab2), [-458, 0, 58, 69, 74, 85, 159])