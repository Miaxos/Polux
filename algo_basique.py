# algo_basique.py in branch structureDeDonnee
# -*- coding: utf-8 -*-

import numpy as np

import utils as struct

from PIL import Image, ImageDraw

def locate(cube, ignoreface, type, color, dico={'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
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
            print(cube.L[j][i])
            print('Face', j, "    ", np.where(cube.L[j][i] == color)[0])
            if type == 1:  # CORNER
                None
            elif type == 2:  # Arrête
                if 1 in (np.where(cube.L[j][i] == color)[0]):
                    return [(i,1,j)]
            i = i+1
        i = 0
        j = j+1
    return None

def affichage(cube):
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
    
def suitemvt(cube, mvt): 
    #mvt : liste des mouvenments à faire ex : ['U','B','2F','R'']

    for i in range(len(mvt)):
        if len(mvt[i]) == 1:
            cube.moveHoraire(mvt[i]) #Le nom des fonctions est provisoire. À changer si besoin
        if len(mvt[i]) == 2:
            if mvt[i][0]=='2':
                cube.moveHoraire(mvt[i][1])
                cube.moveHoraire(mvt[i][1])
            if mvt[i][1]=="'": 
                cube.moveAntiH(mvt[i][0]) #idem

def rearranger_croix(cube): #La croix est déjà formée de base
    enplace = [] #LFRB
    for i in range(1,5):
        if cube.L[i][0][1]==cube.L[i][1][1]: 
            enplace.append(1)               #1 si l arrete est bien place 0 sinon
        else:
            enplace.append(0)
    nbplace =sum(enplace)

    while nbplace<2:             #il y a necessairement 2 arrete bien place
        cube.moveHoraire('u')
        enplace = [] #LFRB
        for i in range(1,5):
            if cube.L[i][0][1]==cube.L[i][1][1]:
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

def isX(cube, face, couleur, dico = {'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
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
    
def wFace_1st_crown(cube):
    '''
    Cette fonction termine la face blanche et fait la 1ère couronne du cube
    '''
    # Tant que la face blanche n'est pas totalement blanche
    while not cube.isX('U','W'):
        # Chercher un coin avec une facette blanche sur toutes autres face hormis la face UP
        corner = cube.locate('U',1,'W')
        # Si le coin trouvé est sur l'étage du bas (3ème couronne + face DOWN) et qu'il n'a pas déjà été pointé
        faceCorner = corner[0][1]
        if 'W' in cube.L[faceCorner][2] or faceCorner == 5:
            # Déplacer la face DOWN de telle sorte que le coin soit directement en dessous de son emplacement finale
                
                
                
    
        
# Exemples :
cube = struct.Cube("OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG")
cube.afficheFaces()
print(cube.locate('URL',2, 'O'))
#cube.affichage()
    # Up + Left + Front + Right + Back + Down (+ : concaténation)

#Exemple CocoM
cube=struct.Cube()
print(cube.isX('L','G'))