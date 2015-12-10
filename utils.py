# utils.py in branch structureDeDonnees
# -*- coding: utf-8 -*-

import numpy as np
<<<<<<< HEAD
=======
from PIL import Image, ImageDraw

>>>>>>> 08cc345398160c58364d5d2ab2d649b4e225c8ed

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
        if (type(mouvement) == str) and (len(mouvement) == 1):
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
            self.L[idFace] = np.array([colonne_1, colonne_2, colonne_3])  # ça fonctionne
            # Pour les autres faces entrainées dans la rotation :
            # si ce sont les faces U ou D :
            if idFace == 0 or idFace == 5:
                if idFace == 0:
                    idRow = 0  # (NB : row = ligne) il faudra bouger toutes les premières lignes des 4 autres faces si on tourne la face UP
                else:
                    idRow = 2  # il faudra bouger toutes les dernières lignes des 4 autres faces si on tourne la face DOWN
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
            elif idFace == 2 or idFace == 4:
                if idFace == 2:
                    idFirstRow = 2
                    idFirstColumn = 2
                else:
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
                self.L[0][idFirstRow] = self.L[1][idFirstColumn]  # face LEFT --> face UP (sens de rotation horaire)
                oldRow = self.L[3][idSecondColumn]
                self.L[3][idSecondColumn] = saveRow  # face UP --> face RIGHT (sens de rotation horaire)
                saveRow = oldRow
                oldRow = self.L[5][idSecondColumn]
                self.L[5][idSecondColumn] = saveRow  # face RIGHT --> face DOWN (sens de rotation horaire)
                saveRow = oldRow
                self.L[1][idSecondColumn] = saveRow  # face DOWN --> face LEFT (sens de rotation horaire)            
            # si ce sont les faces L ou R :
            else:
                # code
                idRow = 0  # TEMPORAIRE, juste là pour que le else ci-dessous ne génère pas une erreur 'expected an indent block'
        else:
            raise TypeError

    def locate(self, ignoreface, type, color, dico={'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
        '''
        ignoreface: str sous la forme (UFD) pour ignorer certaines faces.
        type: 1: corner 2: les autres
        Des qu'il en repère 1 il retourne sa position et la pos de sa liaison(?)

        Return [(pos white, face white), (pos link1, face link1), [(pos link1, face link1) si type 1]]
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
                print('Face', j, "    ", np.where(self.L[j][i] == color)[0])
                if type == 1:  # CORNER
                    None
                elif type == 2:  # Arrête
                    if 1 in (np.where(self.L[j][i] == color)[0]):
                        return [(i,1,j)]
                i = i+1
            i = 0
            j = j+1
        return None
    def affichage(self):
        img = Image.open('a.png')
        img = Image.new( 'RGB', (255,255), (220,220,220)) # create a new black image

        draw = ImageDraw.Draw(img)
        # draw.line((0, 0) + img.size, fill=128)
        # draw.line((0, img.size[1], img.size[0], 0), fill=128)
        draw.rectangle([(28,78),(76,126)],(211,211,211))
        draw.rectangle([(78,78),(126,126)],(211,211,211))
        draw.rectangle([(128,78),(176,126)],(211,211,211))
        draw.rectangle([(178,78),(226,126)],(211,211,211))

        draw.rectangle([(78,28),(126,76)],(211,211,211))
        draw.rectangle([(78,128),(126,176)],(211,211,211))

        draw.rectangle([(78,28),(94,44)], "red")
        draw.rectangle([(94,28),(110,44)], "white")
        draw.rectangle([(110,28),(126,44)], "blue")

        img.show() 
    def suitemvt(self, mvt): 
        #mvt : liste des mouvenments à faire ex : ['U','B','2F','R'']
    
        for i in range(len(mvt)):
            if len(mvt[i]) == 1:
                self.moveHoraire(mvt[i]) #Le nom des fonctions est provisoire. À changer si besoin
            if len(mvt[i]) == 2:
                if mvt[i][0]=='2':
                    self.moveHoraire(mvt[i][1])
                    self.moveHoraire(mvt[i][1])
                if mvt[i][1]=="'": 
                    self.moveAntiH(mvt[i][0]) #idem

    def rearranger_croix(self): #La croix est déjà formée de base
        enplace = [] #LFRB
        for i in range(1,5):
            if self.L[i][0][1]==self.L[i][1][1]: 
                enplace.append(1)               #1 si l arrete est bien place 0 sinon
            else:
                enplace.append(0)
        nbplace =sum(enplace)

        while nbplace<2:             #il y a necessairement 2 arrete bien place
            self.moveHoraire('u')
            enplace = [] #LFRB
            for i in range(1,5):
                if self.L[i][0][1]==self.L[i][1][1]:
                    enplace.append(1)
                else:
                    enplace.append(0)
        nbplace = sum(enplace)
        if not nbT == 4:  # What the fuck is that ? NBT ?
            ## Cas 2 arrêtes en place côte à côte
            if enplace[3] == enplace[0] == True:
                faceact ='R'
            if enplace[0]==enplace[1] == True:
                faceact = 'B'
            if enplace[1]==enplace[2] == True:
                faceact = 'L'
            if enplace[2]==enplace[3]==True:
                faceact = 'F'
            ##Cas 2 arrêtes en place en face
            if enplace[0]==enplace[2]:
                faceact = 'L'
            if enplace[1]==enplace[3]:
                faceact = 'F'

            mvt=[faceact, 'U', faceact + "'", 'U', faceact, 'U2', faceact +"'", 'U']
            suitemvt(mvt)

    def isX(self, face, couleur, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
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
                if self.L[idFace][k][i] != couleur:
                    a = False
        return a
        
        
    def wFace_1st_crown(self):
        '''
        Cette fonction termine la face blanche et fait la 1ère couronne du cube
        '''
        # Tant que la face blanche n'est pas totalement blanche
        while not self.isX('U','W'):
            # Chercher un coin avec une facette blanche sur toutes autres face hormis la face UP
            corner = self.locate('U',1,'W')
            # Si le coin trouvé est sur l'étage du bas (3ème couronne + face DOWN) et qu'il n'a pas déjà été pointé
            faceCorner = corner[0][1]
            if 'W' in self.L[faceCorner][2] or faceCorner == 5:
                # Déplacer la face DOWN de telle sorte que le coin soit directement en dessous de son emplacement finale
                
                
                
    
        
# Exemples :
cube = Cube("OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG")
cube.afficheFaces()
print(cube.locate('URL',2, 'O'))
#cube.affichage()
    # Up + Left + Front + Right + Back + Down (+ : concaténation)

#Exemple CocoM
cube=Cube()
print(cube.isX('L','G'))