import unittest


class TestInput(unittest.TestCase):
    def test_str_input(self):
        mini = 10
        maxi = 20

        self.assertTrue(mini <= len("abcdefghijklmn") <= maxi)
        self.assertFalse(mini <= len("abc"))
        self.assertFalse(maxi >= len("abcedfghijklmnopqrstuvwxyz"))

    def test_number_input(self):
        mini = 10
        maxi = 20

        self.assertTrue(mini <= 10 <= maxi)
        self.assertFalse(mini <= 3)
        self.assertFalse(maxi >= 21)