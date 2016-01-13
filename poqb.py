# poqb.py
# -*- coding: utf-8 -*-

import os
import utils as struct
import algo_basique as alg1

def solve(cube_c54):
    """La fonction principale du projet qui résoud un Rubik's Cube.

    :param cube_c54: passé sous sa forme '54 facettes colorées'
           O G R
           B W Y
           B G B
    G Y Y  O Y O  W O W  G R Y
    O O O  B G B  R R Y  R B W
    W W R  B W Y  G R O  W G R
           Y B R
           G Y W
           B O G
    :return: une chaîne de caractères qui encode la manoeuvre
    qui mène du cube de départ à la permutation monochrome.

    :Example:

    solve('OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG')
    return "R2L'F'DFLD'F2L'F'DFLDBDBL2B'D'BD2L'D'LD'RDR'D2F'D'F2DF'D'FDF'D2RD'R'D'B'DBDBD'B'D'L'DLD'F'DFDLD'L'D'R'DRDFD'LDL'D'F'D2FD'B'DF'D'UBU'B'UBD2B'U'BUB'U'BD'"
    """


    return alg1.solve(cube_c54)


if __name__=="__main__":
    m = input("entrez la chaine de caractère correspondant au cube")    
    print(solve(m))
    os.system("pause")