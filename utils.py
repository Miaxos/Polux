# utils.py in branch structureDeDonnees
# -*- coding: utf-8 -*-

import numpy as np

class Cube:
    '''
    Un cube est défini par sa chaine. Initialement, on considère le cube résolu.
    Tel que la chaine de caractère le définissant soit de type:
    Up + Left + Front + Right + Back + Down (+ : concaténation)
    '''
    def __init__(self, chaine="WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY"):
        '''
        Transforme la chaine de caractère qui définit le cube en une liste qui définit les faces du cube
        '''
        # On pose L
        self.L=[[]]
        
        # Détermination de la face du haut
        for k in range(3): 
            self.L[0].append(list(chaine[0+3*k:3+3*k]))
        # Détermination des faces gauche, devant, droite , derrière
        for k in range(4):                
            self.L.append([list(chaine[9+3*k:12+3*k]),\
                      list(chaine[21+3*k:24+3*k]),\
                      list(chaine[33+3*k:36+3*k])])
        self.L.append([])
        # Détermination de la face de dérrière
        for k in range(3): 
            self.L[5].append(list(chaine[45+3*k:48+3*k]))
        
        # On transforme chacune des faces en tableau numpy     
        for k in range(6):
            self.L[k]=np.array(self.L[k])

        self.L = np.array(self.L)

    def afficheFaces(self):
        print(self.L, '\n', '-----\n')
	
    def moveHoraire(self, mouvement, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
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
            idFace = dico[mouvement.upper()]
            face = np.copy(self.L[idFace])

            # effectuer la rotation d'1/4 de tour horaire sur la face         
            # sélectionnée :
            colonne_1 = [face[k][0] for k in range(-1, -4, -1)]
            colonne_2 = [face[k][1] for k in range(-1, -4, -1)]
            colonne_3 = [face[k][2] for k in range(-1, -4, -1)]

            # les colonnes de la face deviennent ses nouvelles lignes après
            # rotation :
            #face = np.array([colonne_1, colonne_2, colonne_3]) # je ne comprends pas pourquoi l'aliasing ne fonctionne pas
            self.L[idFace] = np.array([colonne_1, colonne_2, colonne_3]) # ça fonctionne

            # Pour les autres faces entrainées dans la rotation :
            # si ce sont les faces U ou D :
            if idFace == 0 or idFace == 5 :
                if idFace == 0 :
                    idRow = 0 # (NB : row = ligne) il faudra bouger toutes les premières lignes des 4 autres faces si on tourne la face UP
                else :
                    idRow = 2 # il faudra bouger toutes les dernières lignes des 4 autres faces si on tourne la face DOWN
                
                # Ce qu'il faut faire (en ayant arbitrairement choisi de
                # commencer par la face 4):
                # save(idRow(4)) ; idRow(1) --> 4 ;
                # save(idRow(3)) ; saved_idRow(4) --> 3 ;
                # save(idRow(2)) ; saved_idRow(3) --> 2 ;
                # saved_idRow(2) --> 1
                # Légende :
                # idRow(x) : sélectionne la ligne d'indice idRow sur la
                # face d'indice x
                # x --> y : insère la ligne x dans la face y

                # On choisit arbitrairement de commencer par la face 4 :
                saveRow = np.copy(self.L[4][idRow])
                self.L[4][idRow] = self.L[1][idRow]
                # puis on repète cela pour les faces 3 à 1 :
                for i in range(3, 0, -1):
                    oldRow = np.copy(self.L[i][idRow])
                    self.L[i][idRow] = saveRow
                    saveRow = oldRow
                    
            # si ce sont les faces F ou B :
            elif idFace == 2 or idFace == 4 :
                if idFace == 2:
                    idFirstRow = 2
                    idFirstColumn = 2
                else :
                    idFirstRow = 0
                    idFirstColumn = 0

                idSecondRow = 2 - idFirstRow
                idSecondColumn = 2 - idFirstColumn
                # En ayant arbitrairement choisi de commencer par la face 0):
                # self.L[0][idFirstRow] # face UP
                # self.L[5][idSecondRow] # face DOWN
                # self.L[1][idFirstColumn] # face LEFT
                # self.L[3][idSecondColumn] # face RIGHT
                saveRow = np.copy(self.L[0][idFirstRow])
                self.L[0][idFirstRow] = self.L[1][idFirstColumn] # face LEFT --> face UP (sens de rotation horaire)

                oldRow = self.L[3][idSecondColumn]
                self.L[3][idSecondColumn] = saveRow # face UP --> face RIGHT (sens de rotation horaire)
                saveRow = oldRow

                oldRow = self.L[5][idSecondColumn]
                self.L[5][idSecondColumn] = saveRow # face RIGHT --> face DOWN (sens de rotation horaire)
                saveRow = oldRow

                self.L[1][idSecondColumn] = saveRow # face DOWN --> face LEFT (sens de rotation horaire)           
            
            # si ce sont les faces L ou R :
            else :
                # code
                idRow = 0 # TEMPORAIRE, juste là pour que le else ci-dessous ne génère pas une erreur 'expected an indent block'
                
        else :
            raise TypeError
    def locate(self, ignoreface, type, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
        '''
        ignoreface: str sous la forme (UFD) pour ignorer certaines faces.
        type: 1: corner 2: les autres
        Des qu'il en repère 1 il retourne sa position et la pos de sa liaison(?)
        '''
        ignoreList = []
        for i in range(0,len(ignoreface)):
            idFace = dico[ignoreface[i].upper()]
            ignoreList.append(idFace)
        print(ignoreList)
        j = 0
        i = 0
        c = False
        while c == False:          
            while i < 3 and not(j in ignoreList):
                print(self.L[j][i])
                print('Face',j,"    ",np.where(self.L[j][i]=='O')[0])
                if len(np.where(self.L[j][i]=='O')[0]) != 0:
                    c = True
                    i = 15
                    print("ZBRA")
                i = i+1
            i = 0
            j = j+1
        
# Exemples :
cube = Cube("123456789abcjklstuABCdefmnovwxDEFghipqryz{GHIJKLMNOPQR")
cube.afficheFaces()
cube.moveHoraire('d')
cube.afficheFaces()
