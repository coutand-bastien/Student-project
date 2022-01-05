def extract_sub(tab:list, number:int) -> list:
    """
        extract the tuple number of the elements of the list

        :param tab: the list in question
        :type: list of tuple(int, list of int)
        :param number: the tuple number
        :type: int

        :return: the sub-list with the tuple number
        :rtype: list
    """
    return [el[number] for el in tab]


def list_to_char(list_to_trad:list) -> str:
    """
        transform a list of numbers 0 <= n <= 255 into a string.

        :param list_to_trad: the list to translate
        :type: list of int

        :return the translated list
        :rtype: str
    """
    return "".join([chr(el) for el in list_to_trad])
