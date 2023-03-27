def str_input(msg: str, mini: int, maxi: int) -> str:
    """
        Requests a string input according to the requested msg. And checks that it is in the min and max range.
        
        :param: msg: the message
        :rtype: str
        :param: mini: the lower limit of the interval
        :rtype: int
        :param: maxi: the upper limit of the interval
        :rtype: int
        
        :return: the user's input
        :rtype: str
    """
    while True:
        string: str = input(msg)
        
        if mini <= len(string) <= maxi:
            break
        else: 
            print(f"MIN: {mini} / MAX: {maxi}")

    return string


def number_input(msg: str, mini: float, maxi: float, t) -> float:
    """
        Requests a int input according to the requested msg. And checks that it is in the min and max range.

        :param: msg: the message
        :rtype: str
        :param: mini: the lower limit of the interval
        :rtype: float
        :param: maxi: the upper limit of the interval
        :rtype: float

        :return: the user's input
        :rtype: float
    """
    while True:
        value: t = t(input(msg))

        if mini <= value <= maxi:
            break
        else:
            print(f"MIN: {mini} / MAX: {maxi}")

    return value
                
