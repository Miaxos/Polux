# poqb.py
# -*- coding: utf-8 -*-

import os
import utils as struct
import algo_basique as alg1

# Exemples :
# un test qui permet de voir que les fonctions modifient bien le cube et que les 
# fonctions horaire et antiHoraire tournent bien.
# On crée donc un cube qui permet de voir le déplacement exact de chaque vignette
# puisqu'elles sont toutes identifiées de manière unique dans la configuration
# de départ :
chaine_conf_unique = "123456789abcjklstuABCdefmnovwxDEFghipqryz{GHIJKLMNOPQR"

def test_1(cube) :
    for i in "udfblr" :
        print("move = " + i.upper())
        cube.moveHoraire(i)
        cube.moveAntiHoraire(i)
        cube.afficheFaces()
        cube = struct.Cube("123456789abcjklstuABCdefmnovwxDEFghipqryz{GHIJKLMNOPQR")

# si les fonctions sont correctes, on devrait avoir le même cube qu'au départ.

# Et un dernier test pour vraiment assurer que les fonctions font bien leur job,
# à l'aide de l'outil fourni sur https://alg.cubing.net
# Leur configuration de départ étant différente de la nôtre, la voici :
chaine_alg_cubing_net = "WWWWWWWWWOOOGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBYYYYYYYYY"

def test_2(cube) :
    for i in 'udb':
        cube.moveHoraire(i)
    for i in 'lrf':
        cube.moveAntiHoraire(i)

# et si les fonctions font bien leur job, on doit retrouver cette configuration
# de couleur pour chaque face :
# https://alg.cubing.net/?setup=UU-&alg=UDBL-R-F-&view=fullscreen

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