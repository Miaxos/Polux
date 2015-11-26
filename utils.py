# utils.py in branch structureDeDonnees
# -*- coding: utf-8 -*-

import numpy as np

class Cube:
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