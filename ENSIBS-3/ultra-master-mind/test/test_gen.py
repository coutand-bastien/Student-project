import sys
import unittest
sys.path.append('../src')

from utils.gen import gen as gen
from utils import constante as const


class TestGen(unittest.TestCase):
    const.dict_const["PM"] = "abc"
    const.dict_const["L"] = len(const.dict_const.get("PM"))

    def test_genese(self):
        # const.dict_const["N"] = -5
        # gen.genese()  # AssertionError

        const.dict_const["N"] = 10
        seq_init = gen.genese()

        self.assertTrue(seq_init != [])
        self.assertTrue(len(seq_init) == const.dict_const.get("N"))
        self.assertTrue(len(seq_init[0]) == const.dict_const.get("L"))

    def test_fitness_distance(self):
        res = gen.fitness_distance([100, 98, 101])  # dbe
        self.assertTrue(res < 0)  # res = -5

        res = gen.fitness_distance([97, 98, 99])  # abc
        self.assertTrue(res == 0)

    def test_fitness_max_weight(self):
        res1 = gen.fitness_max_weight([100, 98, 101])  # dbe
        res2 = gen.fitness_max_weight([97, 98, 99])  # abc

        self.assertTrue(res1 < res2)
        self.assertTrue(res2 == (len(const.dict_const.get("PM") * 10)))  # 10 pt for good answers

    def test_fitness_levenshtein(self):
        res1 = gen.fitness_levenshtein([100, 98, 101])  # dbe
        res2 = gen.fitness_levenshtein([97, 98, 99])  # abc

        self.assertTrue(res1 > 0, )  # res1 = 2
        self.assertTrue(res2 == 0)

    def test_selection(self):
        const.dict_const["N"] = 3
        test_pop = [[100, 98, 101], [101, 99, 102], [100, 99, 101]]  # [[dbe], [ecf], [dce]]

        self.assertEqual(gen.selection(test_pop)[0], [[100, 98, 101]])  # dbe

    def test_reproduction(self):
        const.dict_const["N"] = 10
        test_pop = [[100, 98, 101], [101, 99, 102], [100, 99, 101]]  # [[dbe], [ecf], [dce]]

        self.assertNotEqual(len(test_pop), const.dict_const.get("N"))

        new_gen = gen.reproduction(test_pop)

        self.assertEqual(len(new_gen), const.dict_const.get("N"))
        self.assertTrue((test_pop[0] in new_gen) & (test_pop[1] in new_gen) & (test_pop[2] in new_gen))

    def test_mutation(self):
        const.dict_const["N"] = 3
        const.dict_const["TM"] = 1

        """
            Forced to make two separate lists because the mutation function uses a procedure and therefore changes the 
            list. It would be possible to make only one list if we made a deep copy with for example the module copy and 
            its function deepcopy(list) 
        """
        test_pop_origin = [[100, 98, 101], [101, 99, 102], [100, 99, 101]]  # [[dbe], [ecf], [dce]]

        self.assertNotEqual(test_pop_origin, gen.mutation([[100, 98, 101], [101, 99, 102], [100, 99, 101]]))

    def test_evolution(self):
        test_pop_origin = gen.genese()

        test_pop_evolve = gen.evolution(test_pop_origin)
        self.assertNotEqual(test_pop_origin, test_pop_evolve)
