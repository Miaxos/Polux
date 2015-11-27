# utils.py in branch structureDeDonnees
# -*- coding: utf-8 -*-

import numpy as np

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
        
        self.L=[[]]             # On pose L
        
        for k in range(3):                  # Détermination de la face du haut
            self.L[0].append(list(chaine[0+3*k:3+3*k]))
        for k in range(4):                  # Détermination des faces gauche, devant, droite , derrière
            self.L.append([list(chaine[9+3*k:12+3*k]),\
                      list(chaine[21+3*k:24+3*k]),\
                      list(chaine[33+3*k:36+3*k])])
        self.L.append([])
        for k in range(3):                  # Détermination de la face de dérrière
            self.L[5].append(list(chaine[45+3*k:48+3*k]))
            
        for k in range(6):                  # On transforme chacune des faces en tableau numpy 
            self.L[k]=np.array(self.L[k])

        self.L = np.array(self.L)
        
    def afficheFaces(self):
        print(self.L, '\n', '-----\n')
	
    def move(self, mouvement, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
        """
        moveSeq(String) - moves the Cube with the given pattern, ON PLACE
        
        :param mouvement: String de longueur 1
        :param dico: dictionnaire des faces/mouvements (étant donné qu'un nom
        de mouvement correspond à une face, on appelle ce dictionnaire comme
        on veut).
        À propos des dictionnaires : leur structure est la suivante :
        chaque élément d'un dictionnaire est un couple clé/valeur dont la
        syntaxe est clé:valeur .
        La commande nomDico[nomClé] renvoie la valeur associée à cette clé.
        """
        
        if (type(mouvement) == str) and (len(mouvement) == 1) :
            # récupérer la face associée au mouvement :
            face = self.L[dico[mouvement.upper()]]

            # effectuer la rotation d'1/4 de tour horaire sur la face         
            # sélectionnée :
            colonne_1 = [face[0] for k in range(-1, -4, -1)]
            colonne_2 = [face[1] for k in range(-1, -4, -1)]
            colonne_3 = [face[2] for k in range(-1, -4, -1)]

            # les colonnes de la face deviennent ses nouvelles lignes après
            # rotation :
            face = np.array([colonne_1, colonne_2, colonne_3])          
        
        else :
            raise TypeError
        
# Exemples :
cube = Cube("123456789GGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY")
cube.afficheFaces()
cube.move('u')
cube.afficheFaces()