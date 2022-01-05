import random as rand
import statistics as stats
import math

from utils.sort import sort as sort
from utils import constante as const
from utils.transform import transform as trans


def genese() -> list:
    """
        Create the initial population. len(person) = len(PM)

        :return: random population of size N and length of individual of size L = len(PM)
        :rtype: list of list of int
    """
    sequence: list = []

    for i in range(const.dict_const.get("N")):
        person: list = []
        for j in range(const.dict_const.get("L")):
            person.append(rand.randint(0, 255))

        sequence.append(person)

    return sequence


def fitness_distance(C:list) -> int:
    """
        Function that calculates the distance of the C chromosome from the mystery sentence.
        Formula: -Σ(|C[i]-PM[i]|), i=0..(L-1)
        
        Domain: [-inf, 0]
                            Lim fitness_distance(C)   ----> 0
                            C --> solution

        :param C: the looked chromosome
        :type: list of int

        :return: an integer
        :rtype: int
    """
    res: int = 0

    for i in range(const.dict_const.get("L")):
        res += abs(C[i] - ord(const.dict_const.get("PM")[i]))

    return -res


def fitness_max_weight(C:list) -> int:
    """
        Function that calculates the sum of the weights of the C chromosome with respect to the mystery phrase.
        Formula for a character #MissedPlaced(val:1) + #Match(val:9)
        
        Domain: [0, +inf]
                            Lim fitness_max_weight(C)   ----> +inf
                            C --> solution

        :param C: the looked chromosome
        :type: list of int

        :return: an integer
        :rtype: int
    """
    res: int = 0
    pm_tmp: str = const.dict_const.get("PM")
    i: int = 0

    while i < const.dict_const.get("L"):
        if chr(C[i]) in pm_tmp:
            res += 1  # MissedPlaced

            if C[i] == ord(const.dict_const.get("PM")[i]): res += 9  # Match

            pm_tmp = pm_tmp.replace(chr(C[i]), '', 1)  # delete the first value of pm_tmp

        i += 1

    return res

def fitness_levenshtein(c: list) -> int:
    """
        We call the Levenshtein distance between two strings M and P the minimal cost to transform M into P by performing
        only elementary operations (at the level of a character). Elementary operations: substitution / insertion (or
        addition) / deletion (or erasure).

        Domain: [0, +inf]

                        Lim fitness_levenshtein(C)   ----> 0
                        C --> solution

        :param c: the looked chromosome
        :type: list of int

        :return: the number of operation necessary to pass from the string C to PM.
        :rtype: int
    """
    return dist_levenshtein(c, const.dict_const.get("PM"))


def dist_levenshtein(c: list, pm: str) -> int:
    previous_row = range(len(pm) + 1)

    for i, c1 in enumerate(c):
        current_row: list[int] = [i + 1]

        for j, c2 in enumerate(pm):
            # in the order : insertion, deletion, substitution
            current_row.append(min(previous_row[j + 1] + 1, current_row[j] + 1, previous_row[j] + (chr(c1) != c2)))
        previous_row = current_row

    return previous_row[-1]


def selection(pop:list) -> tuple[list, int]:
    """
        all the individuals of the population have a chromosome. The individuals are classified according to the value 
        provided by the function Fitness. The TS x N best individuals are selected for the reproduction. The
        others are deleted, they will be replaced by the descendants created by reproduction. 
        
        :param pop: The population base
        :type: list of list of int

        :return: the selection of the best individuals of the pop
        :rtype: tuple[list, int]
    """
    res: list = []

    dict_choice = {
        1: fitness_distance,
        2: fitness_max_weight,
        3: fitness_levenshtein
    }

    for i in range(const.dict_const.get("N")):
        # Choice of fitness to use
        score: int = dict_choice.get(const.dict_const.get("FITNESS_CHOICE"))(pop[i])

        if (const.dict_const.get("FITNESS_CHOICE") != 2 and score == 0) or (const.dict_const.get("FITNESS_CHOICE") == 2 and score == const.dict_const.get("L") * 10):
            return [pop[i]], 0  # score = 0 because word is found

        res.append((score, pop[i]))  # (score, el)

    # grow for levenshtein and decrease for the other (see limits in rapport)
    res: list = sort.fusion_sort_decreasing(res) if const.dict_const.get("FITNESS_CHOICE") != 3 else sort.fusion_sort_growing(res)

    score_pop_list = trans.extract_sub(res, 0)  # all score of the population
    print(f"[mean: {stats.mean(score_pop_list)} - score: {score_pop_list[0]} ]\t\t\t {trans.list_to_char(res[0][1])}")  # display the best chromosome

    return trans.extract_sub(res[:math.ceil(const.dict_const.get("N") * const.dict_const.get("TS"))], 1), score_pop_list[0]


def reproduction(pop:list) -> list:
    """
        two individuals P and M are randomly drawn from the selected individuals.
        selected individuals. We draw 2 points of cut: cut1 = L * (1/3) and cut2 = L * (2/3). We
        a new chromosome (individuals) CM as follows.
        
                            CM = concatenation(P[:(1/3)], M[(1/3):(2/3)] + P[(2/3):])
                            
        The new individual is added to the population : we iterate the procedure
        in order to find a population of N individuals.
        
        :param pop: the population to be reproduced
        :type: list of list of int

        :return: the population and its descendants
        :rtype: list of list of int
    """
    start_size: int = len(pop) - 1

    while len(pop) != const.dict_const.get("N"):
        # p and m must not be equal
        while True:
            p: int = rand.randint(0, start_size)
            m: int = rand.randint(0, start_size)
            if p != m: break

        cut1: int = int(1 / 3 * const.dict_const.get("L"))
        cut2: int = int(2 / 3 * const.dict_const.get("L"))
        pop.append(pop[p][:cut1] + pop[m][cut1:cut2] + pop[p][cut2:])

    return pop


def mutation(pop:list) -> None:
    """
        We select at random TM x N individuals on which the mutation of a mutation of a gene will be carried. For each 
        selected individual, we draw at random a gene a gene (a character) among L and we randomly randomly change its value
        
        :param pop: the population to mutate
        :type: list of list of int
    """
    nb_rand_ind: int = rand.randint(0, math.ceil(const.dict_const.get("TM") * const.dict_const.get("N")))  # number of chromosome who have benn changed

    while nb_rand_ind > 0:
        rand_pop : int = rand.randint(0, const.dict_const.get("N") - 1)
        rand_gene: int = rand.randint(0, const.dict_const.get("L") - 1)
        pop[rand_pop][rand_gene] = rand.randint(0, 255)
        nb_rand_ind -= 1


def evolution(pop:list) -> tuple[list, int]:
    """
        over several generations :
            - Evaluation of the individuals in the population
            - Selection of a part of the population
            - Reproduction by crossing of some individuals
            - Mutation of certain individuals

        :param pop: The population to evolve
        :type: list of list of int

        :return: a new version of the population, closer to PM.
        :rtype: tuple[list, int]
    """
    tuple_values: tuple[list, int] = selection(pop)
    new_pop: list = tuple_values[0]

    if (len(new_pop) == 1) and (trans.list_to_char(new_pop[0]) == const.dict_const.get("PM")):
        return [], 0 if const.dict_const["FITNESS_CHOICE"] != 2 else const.dict_const.get("L") * 10  # score = 0 because word is found

    reprod_pop: list = reproduction(new_pop)
    mutation(reprod_pop)

    return reprod_pop, tuple_values[1]