# utils.py in branch structureDeDonnees
# -*- coding: utf-8 -*-

import numpy as np

def colonne_en_ligne(idColonne, face, fin_plage = 3, debut_plage = 0, pas_plage = 1):
    """
    Renvoie les éléments de la colonne d'indice x d'une face donnée au format d'une ligne.
    Les 3 derniers paramètres servent à sélectionner la colonne de haut en bas
    ou de bas en haut.
    """
    return np.array([face[k][idColonne] for k in range(debut_plage, fin_plage,
                                               pas_plage)])

def revert_ligne(idLigne, face):
    copie = np.copy(face[idLigne])
    for k in range(3):
        face[idLigne][k] = copie[-k - 1]

def revert_colonne(idColonne, face):
    copie = np.array([face[k][idColonne] for k in range(3)])
    for k in range(3):
        face[k][idColonne] = copie[-k - 1]

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
        self.chaine = chaine       
        if len(chaine) == 54 :
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
        
        else :
            raise ValueError("chaine trop courte !")


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
        self.move(mouvement, "horaire")

    def moveAntiHoraire(self, mouvement, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
        self.move(mouvement, "antiHoraire")


    def move_vignettes(self, idFace, sens):
        """
        Docstring
        Basé sur la remarque que pour toutes les faces ont le même mouvement
        de vignettes "internes" (les auto-collants qui composent la face)
        """
        
        face = np.copy(self.L[idFace])
        
        if sens == "horaire" :
            debut_plage = -1
            fin_plage = -4
            pas_plage = -1
            idPremiereLigne = 0
            idDerniereLigne = 2

        else :
            debut_plage = 0
            fin_plage = 3
            pas_plage = 1
            idPremiereLigne = 2
            idDerniereLigne = 0

        self.L[idFace] = np.array([colonne_en_ligne(idPremiereLigne, face, fin_plage,
                                           debut_plage, pas_plage),
                                   colonne_en_ligne(1, face, fin_plage,
                                           debut_plage, pas_plage),
                                   colonne_en_ligne(idDerniereLigne, face, fin_plage,
                                           debut_plage, pas_plage)])


    def move_U(self, sens, idRow = 0):
        """
        Docstring
        on conserve le même ordre entre les listes lors d'un passage d'une face
        à l'autre
        """

        if sens == "horaire" :
            cycle = [4,3,2,1,4]

        else :
            cycle = [4,1,2,3,4]
            
        oldRow = np.copy(self.L[cycle[0]][idRow])
        
        for j in range(1, len(cycle)) :
            i = cycle[j]
            
            saveRow = np.copy(self.L[i][idRow])
            self.L[i][idRow] = np.copy(oldRow)
            oldRow = np.copy(saveRow)

    def move_D(self, sens):
        """
        Docstring
        """
        if sens == "horaire" :
            self.move_U("antiHoraire", 2)
        else :
            self.move_U("horaire", 2)


    def move_F(self, sens, indicateur = "front"):
        """
        Docstring
        """
        if sens == "horaire":
            cycle = [0,3,5,1,0]
            if indicateur == "bottom" :
                position = [0,2,2,0,0]
            else :
                position = [2,0,0,2,2]

        else :
            cycle = [0,1,5,3,0]
            if indicateur == "bottom" :
                position = [0,0,2,2,0] 
            else :
                position = [2,2,0,0,2]
            
        old = np.copy(self.L[cycle[0]][position[0]].reshape((3,1)))

        for j in range(1, len(cycle)):
            i = cycle[j]
            pos = position[j]

            if j%2 != 0 :
                # le cycle commence par un changement une ligne en une colonne
                save = np.copy(colonne_en_ligne(pos, self.L[i], -4, -1, -1))
                for k in range(3) :
                    self.L[i][k][pos] = old[k][0] # le reshape ajoute une dimenion à l'array "old"
                old = np.copy(save)
                
                if sens == "antiHoraire" :
                    revert_colonne(pos, self.L[i])
                
            else :
                save = np.copy(self.L[i][pos]).reshape((3,1))
                self.L[i][pos] = np.copy(old)
                old = np.copy(save)

                if sens == "antiHoraire" :
                    revert_ligne(pos, self.L[i])

    def move_B(self, sens):
        """
        Docstring
        """
        if sens == "horaire" :
            self.move_F("antiHoraire", "bottom")
        else :
            self.move_F("horaire", "bottom")


    def move_L(self, sens, idColumn = 0):
        if sens == "horaire" :
            cycle = [0,2,5,4,0]
        else :
            cycle = [0,4,5,2,0]

        old = colonne_en_ligne(idColumn, self.L[cycle[0]])
        
        for j in range(1, len(cycle)) :
            i = cycle[j]
        
            if i == 4 :
                save = colonne_en_ligne(2 - idColumn, self.L[i])
                for k in range(3) :
                    self.L[i][k][2 - idColumn] = old[-k - 1]

                for k in range(3):
                    old[k] = save[-k - 1]

            else :
                save = colonne_en_ligne(idColumn, self.L[i])
                for k in range(3) :
                    self.L[i][k][idColumn] = old[k]
                old = np.copy(save)
                                             
    def move_R(self, sens):
        if sens == "horaire":
            self.move_L("antiHoraire", 2)
        else :
            self.move_L("horaire", 2)

    
    def move(self, mouvement, sens, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
        """
        Docstring
        """
        if (type(sens) == str) and (sens == "horaire" or sens == "antiHoraire") :

            if (type(mouvement) == str) and (len(mouvement) == 1) :
                idFace = dico[mouvement.upper()]
                self.move_vignettes(idFace, sens)

                if idFace == 0 :
                    self.move_U(sens)

                elif idFace == 5 :
                    self.move_D(sens)



                elif idFace == 2 :
                    self.move_F(sens)
        
                elif idFace == 4 :
                    self.move_B(sens)



                elif idFace == 1 :
                    self.move_L(sens)

                elif idFace == 3 :
                    self.move_R(sens)

            else :
                raise TypeError("mouvement inconnu")

        else :
            raise TypeError("sens inconnu")