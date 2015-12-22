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


    def isFull(cube, face, couleur, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
        '''
        Cette fonction détermine si la face est totalement de la couleur demandé
        Elle renvoie donc un booléen
        
        face : str de la face a testée
        couleur : str de la couleur voulu
        '''
        # On suppose que la réponse est Vrai
        a = True
        idFace = dico[face.upper()]
        # Pour toutes les lignes de la face
        for k in range(3):
            # Pour toutes les élèments de chaque ligne
            for i in range(3):
                # Si on trouve une facette qui n'est pas de la bonne couleur on renvoie Faux
                if cube.L[idFace][k][i] != couleur:
                    a = False
        return a


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
            # pour une meilleure lisibilité du code :
            face = np.copy(self.L[idFace])

            # effectuer la rotation d'1/4 de tour horaire sur la face         
            # sélectionnée :
            colonne_1 = [face[k][0] for k in range(-1, -4, -1)]
            colonne_2 = [face[k][1] for k in range(-1, -4, -1)]
            colonne_3 = [face[k][2] for k in range(-1, -4, -1)]

            # les colonnes de la face deviennent ses nouvelles lignes après
            # rotation :
            ##face = np.array([colonne_1, colonne_2, colonne_3]) # je ne comprends pas pourquoi l'aliasing ne fonctionne pas
            self.L[idFace] = np.array([colonne_1, colonne_2, colonne_3]) # ça fonctionne

            # Pour les autres faces entrainées dans la rotation :

            # /!\ la face BACK est la SEULE face qui soit inversée suivant
            # la vue.
            # En effet, sur une vue plane (éclatée), la première colonne de la
            # face BACK en partant de la gauche n'est pas la première colonne
            # de la face BACK en 3D, mais la 3ème...
            
            # si mouvement est U ou D :
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
                # x --> y : insère la ligne x dans la face d'indice y

                # On choisit arbitrairement de commencer par la face 4 :
                saveRow = np.copy(self.L[4][idRow])
                self.L[4][2 - idRow] = self.L[1][idRow]
                # puis on repète cela pour les faces 3 à 1 (sens horaire) :
                for i in range(3, 0, -1) :
                    oldRow = np.copy(self.L[i][idRow])
                    # on conserve le même ordre entre les listes
                    self.L[i][idRow] = saveRow
                    saveRow = oldRow
                    
            # si mouvement est F ou B :
            elif idFace == 2 or idFace == 4 :
            # sur les faces UP & DOWN, il faudra déplacer des lignes uniquement,
            # soit la première soit la dernière en fonction de si la rotation
            # est F ou B et en fonction de si la face concernée est UP ou DOWN.
            # D'où idFirstRow et idSecondRow qui correspondent à ces indices
            # de ligfne "changeant".
            # De même pour idFirstColumn et idSecondColumn.
            # C'est aussi ce qui empêche d'automatiser le processus avec une
            # boucle for.
                if idFace == 2:
                    # l'indice de la ligne de UP que l'on déplacera :
                    idFirstRow = 2
                    # l'indice de la colonne de LEFT que l'on déplacera :
                    idFirstColumn = 2
                else :
                    idFirstRow = 0
                    idFirstColumn = 0

                # l'indice de la ligne de DOWN que l'on déplacera, qui est le
                # complément à 2 de l'indice de la ligne déplacée de la face
                # UP :
                idSecondRow = 2 - idFirstRow
                # l'indice de la colonne de RIGHT que l'on déplacera, qui est
                # le complément à 2 de l'indice de la colonne déplacée de la
                # face LEFT :
                idSecondColumn = 2 - idFirstColumn

                # On choisit arbitrairement de commencer la rotation par la
                # face UP :
                # sauvegarde de la ligne de la face UP amenée à être remplacée
                # à la fin de la rotation :
                saveRow = np.copy(self.L[0][idFirstRow])
                # face LEFT --> face UP (sens de rotation horaire) :
                self.L[0][idFirstRow] = [self.L[1][k][idFirstColumn] for k in \
                                         range(-1, -4, -1)]

                # sauvegarde de la colonne de la face RIGHT amenée à être
                # remplacée à la fin de la rotation :
                oldRow = np.copy([self.L[3][k][idSecondColumn] for k in \
                                  range(3)])
                # face UP --> face RIGHT (sens de rotation horaire) :
                for k in range(3) :
                    # on conserve l'ordre des listes :
                    self.L[3][k][idSecondColumn] = saveRow[k] 
                saveRow = oldRow

                # sauvegarde de la face DOWN :
                oldRow = np.copy(self.L[5][idSecondRow])
                # face RIGHT --> face DOWN (sens de rotation horaire) :
                self.L[5][idSecondRow] = saveRow 
                for k in range(-1, -4, -1) :
                    # on inverse l'ordre des listes (-k - 1 varie de 0 à 3) :
                    self.L[5][idSecondRow][-k - 1] = saveRow[k] 
                saveRow = oldRow
                
                # face DOWN --> face LEFT (sens de rotation horaire) :
                for k in range(3) :
                    # on conserve l'ordre des listes :
                    self.L[1][k][idSecondColumn] = saveRow[k]
            
            # si mouvement est L :
            elif idFace == 1 :
                # la couronne est composée de colonnes uniquement :
                idColumn = 0

                # Les remplacements à effectuer :
                # face BACK --> face UP                    
                # face UP --> face FRONT
                # face FRONT --> face DOWN
                # face DOWN --> face BACK
                
                # On choisit arbitrairement de commencer la rotation par la
                # face UP :
                # sauvegarde de la face UP :
                saveColumn = np.copy([self.L[0][k][idColumn] for k in \
                                   range(3)])
                # face BACK --> face UP (sens de rotation horaire) :
                for k in range(-1, -4, -1) :
                    # on inverse l'ordre des listes (-k - 1 varie de 0 à 3) :
                    self.L[0][-k - 1][idColumn] = self.L[4][k][2 - idColumn]

                # même processus pour les remplacements suivants :
                # UP --> FRONT,
                # FRONT --> DOWN
                # en respectant le sens horaire :
                for j in [2, 5] :
                    # sauvegarde de la face j
                    oldColumn = np.copy([self.L[j][k][idColumn] for k in \
                                   range(3)])
                                        
                    for k in range(3) :
                        # on conserve l'ordre des listes :
                        self.L[j][k][idColumn] = saveColumn[k]
                    saveColumn = oldColumn

                # On est obligé de faire le mouvement DOWN --> BACK "à la main",
                # à cause du décalage d'indice de cette face.
                for k in range(3):
                    # on conserve l'ordre des listes :
                    self.L[4][k][2 - idColumn] = saveColumn[k]                   

                    
            # si mouvement est R :
            elif idFace == 3 :
                # la couronne est composée de colonnes uniquement :
                idColumn = 2
                
                # face FRONT --> face UP
                # face UP --> face BACK
                # face BACK --> face DOWN
                # face DOWN --> face FRONT
                
                # On choisit arbitrairement de commencer la rotation par la
                # face UP :
                # sauvegarde de la face UP :
                saveColumn = np.copy([self.L[0][k][idColumn] for k in \
                                   range(3)])
                # face FRONT --> face UP (sens de rotation horaire) :
                for k in range(3) :
                    # on conserve l'ordre des listes :
                    self.L[0][k][idColumn] = self.L[2][k][idColumn]

                # sauvegarde BACK :
                oldColumn = np.copy([self.L[4][k][2 - idColumn] for k in \
                                   range(3)])
                # face UP --> face BACK :               
                for k in range(-1, -4, -1) :
                    # on inverse l'ordre des listes (-k - 1 varie de 0 à 3) :
                    self.L[4][-k - 1][2 - idColumn] = saveColumn[k]
                saveColumn = oldColumn

                # sauvegarde DOWN :
                oldColumn = np.copy([self.L[5][k][idColumn] for k in \
                                   range(3)])                
                # face BACK --> face DOWN :
                for k in range(-1, -4, -1) :
                    # on inverse l'ordre des listes (-k - 1 varie de 0 à 3) :
                    self.L[5][-k - 1][idColumn] = saveColumn[k]
                saveColumn = oldColumn

                # sauvegarde FRONT :
                oldColumn = np.copy([self.L[2][k][idColumn] for k in \
                                   range(3)])                
                # face DOWN --> face FRONT :
                for k in range(3) :
                    # on conserve l'ordre des listes :
                    self.L[2][k][idColumn] = saveColumn[k]
                
        else :
            raise TypeError
