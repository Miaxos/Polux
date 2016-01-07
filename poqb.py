# poqb.py
# -*- coding: utf-8 -*-

import utils as struct

# Exemples :
# un cube qui permet de voir le déplacement exact de chaque vignette
# puisqu'elles sont toutes identifiées de manière unique dans la configuration
# de départ :
cube = struct.Cube("123456789abcjklstuABCdefmnovwxDEFghipqryz{GHIJKLMNOPQR")

cube.afficheFaces()
for i in 'udfblr' :
    print("move = " + i.upper())
    cube.moveHoraire(i)
    cube.moveAntiHoraire(i)
    cube.afficheFaces()
    cube = struct.Cube("123456789abcjklstuABCdefmnovwxDEFghipqryz{GHIJKLMNOPQR")

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

    pass
    return "ch'sais pas faire..."


if __name__=="__main__":
    cube = 'OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG'
    print ("Pour la résolution de {}\nExécuter la manoeuvre {}".format(cube, solve(cube)))