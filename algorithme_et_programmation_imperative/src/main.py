"""
    :nameProject: UMM

    :project: We consider a string of any length L (mystery sentence). The characters are ascii codes coded on a
               byte from 0 to 255 (alphabet of 256 characters) The game consists in discovering the mystery sentence.
               The player submits sentences of length L, and the system answers by simply indicating the number of the
               number of characters in match and the number of misplaced characters (miss placed).

    :partOfTheProject: project as part of courses at the University of south brittany.

    :lastUpdate: 27 november 2021.

    :Author: COUTAND Bastien (coutand.e2100676@etud.univ-ubd.fr)
"""
import sys

from run import *

def main() -> int:
    run()
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit