# poqb.py
# -*- coding: utf-8 -*-

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

    """

    pass
    return "ch'sais pas faire..."


if __name__=="__main__":
    cube = 'OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG'
    print ("Pour la résolution de {}\nExécuter la manoeuvre {}".format(cube, solve(cube)))

class Cube:
    '''
    Un cube est défini par sa chaine. Initialement, on considère le cube résolu.
    Tel que la chaine de caractère le définissant soit de type:
    Up + Left + Front + Right + Back + Down (+ : concténation)
    '''
    def __init__(self, chaine="WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY"):
        '''
        Transforme la chaine de caractère qui définit le cube en une liste qui définit les faces du cube
        '''
        ch = []
        for k in chaine:
            ch.append(k)
        self.L=[[]]
        
        for k in range(3):
            self.L[0].append([list(chaine[0+3*k:3+3*k])])
        for k in range(4):
            self.L.append([list(chaine[9+3*k:12+3*k]),\
                      list(chaine[21+3*k:24+3*k]),\
                      list(chaine[33+3*k:36+3*k])])
        self.L.append([])
        for k in range(3):
            self.L[5].append([list(chaine[45+3*k:48+3*k])])
    
    def afficheFaces(self):
        print(self.L)
            