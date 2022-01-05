import math
import time
import matplotlib.pyplot as plt

from utils import constante as const
from utils.input import input as ipt
from utils.gen import gen as gen


def __start_run__() -> None:
    """
        User choose the start of the program
    """
    start_choice = ipt.number_input(
        "\nPlease select:"
        "\n 1 - Basic parameters"
        "\n 2 - Choose your parameters"
        "\n"
        "\nChoice: ",
        1, 2, int
    )

    # if user choose 2
    if start_choice == 2:
        pm: str = ipt.str_input("Please choose the mystery phrase: ", 10, 50)
        const.dict_const["PM"] = pm
        const.dict_const["L"]  = len(pm)

        const.dict_const["N"]  = ipt.number_input("Please choose the number of chromosome: ", 10, math.inf, int)
        const.dict_const["TS"] = ipt.number_input("Please choose the selection rate: ", 0.1, 1, float)
        const.dict_const["TM"] = ipt.number_input("Please choose the mutation rate: ", 0.1, 1, float)
        const.dict_const["NG"] = ipt.number_input("Please choose the number of generation: ", 1, math.inf, int)
        const.dict_const["FITNESS_CHOICE"] = ipt.number_input(
            "Please choose the fitness:"
            "\n 1 - fitness_distance"
            "\n 2 - fitness_max_weight"
            "\n 3 - fitness levenshtein rec"
            "\n"
            "\nChoice: "
            , 1, 3, int
        )

    # list all the parameters
    print("List of parameters:")
    print("\n".join([f"{key} = {val}" for key, val in const.dict_const.items()]))

    # asks the user if he wants to display the curves
    while True:
        curve_choice: str = input("\nDisplay curve? (o/N) ").lower()

        if curve_choice in ["o", "n"]:
            const.dict_const["CURVE_CHOICE"] = 1 if curve_choice == "o" else 0
            break


def run() -> None:
    """
        projet_API launch function
    """
    while True:
        __start_run__()

        ng: int = const.dict_const.get("NG")
        y_curve_values: list = []  # use for trace the curve

        start_time: float = time.time()  # START OF TIME CALCULATE


        ############################################
        #                GAME LOOP
        ############################################

        umm: list = gen.genese()

        while umm and ng != 0:
            tuple_values: tuple[list, int] = gen.evolution(umm)
            umm: list = tuple_values[0]

            y_curve_values.append(tuple_values[1] if const.dict_const.get("FITNESS_CHOICE") != 1 else -tuple_values[1])  # -tuple_values because the first fitness use se negative sum
            ng -= 1

        if not umm:
            print(f"End, the word has been found !!! [ {const.dict_const.get('PM')} ] in {const.dict_const.get('NG') - ng} generations")
        else:
            print(f"End of the {const.dict_const.get('NG')} generations, the secret word isn't found")

        ############################################
        #              END GAME LOOP
        ############################################


        delta_time: float = time.time() - start_time  # END OF TIME CALCULATE

        if const.dict_const["CURVE_CHOICE"]:
            plt.plot(range(len(y_curve_values)), y_curve_values, label="fitness_curve")
            plt.title("Result of the UMM according to the number of generations")
            plt.xlabel("number of generations")
            plt.ylabel("fitness score")
            plt.legend()

            plt.show()

        print(f"\ntime: {delta_time} s")



        ############################################
        #               EXIT OR NOT
        ############################################

        if input("Do you want to restart the game? (o/N)").lower() == 'n':
            break
