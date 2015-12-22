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
    #mvt : chaine
    #cube :declass cube
    for i in range(len(mvt)):
        if mvt[i] in ['U', 'L', 'F', 'R', 'B', 'D']:
            if mvt[i+1] == 2:
                cube.moveHoraire(mvt[i])
                cube.moveHoraire(mvt[i])
            elif mvt[i+1]=="'":
                cube.moveAntiH(mvt[i]) #Nom de la fonction a changer si besoin
            else:
                cube.moveHoraire(mvt[i])

def rearranger_croix(cube, faceup):
    '''
    Permet de mettre les arrete de la croix des face up et down a leur place
    La croix est déjà formée de base
    faceup : boleen pour differencier face up et down (croix de différente manière)
    '''
    if faceup:
        face = 'U'
        idplace = 0
    else:
        face = 'D'
        idplace = 2

    nbplace=0
    while nbplace<2: #il y a necessairement 2 arrete bien place
        enplace = [] #les positions dans la liste correspondent aux différentes faces
        for i in range(1,5):
            if cube.L[i][idplace][1]==cube.L[i][1][1]:
                enplace.append(1)
            else:
                enplace.append(0)
            nbplace = sum(enplace)
        if nbplace < 2:
            cube.moveHoraire(face)

    if nbplace != 4 and faceup: #si les 4 sont bien placé, rien a faire
        ## Cas 2 arrêtes en place côte à côte
        if enplace[3] == enplace[0] == 1:
            if faceup: #c'est plus opimise niveau mouvment si on considere differremment les face up  et down
                mvt ="RU'R'U'R"
            else:
                mvt ="FD2F'D'FD'F'D'"
        if enplace[0]==enplace[1] == 1:
            if faceup:
                mvt = "BU'B'U'B"
            else:
                "RD2R'D'RD'R'D'"
        if enplace[1]==enplace[2] == 1:
            if faceup:
                mvt = "LU'L'U'L"
            else:
                mvt = "BD2B'D'BD'B'D'"
        if enplace[2]==enplace[3]==1:
            if faceup:
                mvt = "FU'F'U'F"
            else:
                mvt = "LD2L'D'LD'L'D'"

        ##Cas 2 arrêtes en place en face
        if enplace[0]==enplace[2]:
            if faceup:
                mvt = "LU2L'U2L"
            else:
                mvt = "LD2L'D'LD'L'FD2F'D'FD'F'D'"
        if enplace[1]==enplace[3]:
            if faceup:
                mvt = "FU2F'U2F"
            else:
                mvt = "FD2F'D'FD'D'LD2L'D'LD'L'D'"
        suitemvt(mvt)

def cornerInPlace(cube, positionCoin, couleurCoin, dico={'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}, dico2={'W':0, 'G':1, 'R':2, 'B':3, 'O':4, 'Y':5}):
    '''
    Si le coin n'est pas situé en dessous de son emplacement final, la fonction tourne la face DOWN
    du cube de tel sorte qu'il soit alors à la bonne place. Si le coin est déjà bien placé, elle retourne True.
    
    positionCoin : chaine de 3 caractère ( Ex : "LFD" ) 
    couleurCoin  : chaine de 3 caractère ( Ex : "WBR" )
    
    Dans l'exemple : sur la face Left le coin est White, sur la face Front le coin est Bleu, etc...
    '''
    positionCoinN=[]
    couleurCoinN=[]
    for k in range(3):
        # Transcrit les lettres en valeurs décimal (voir support papier pour explication)
        positionCoinN.append(dico[positionCoin[k].upper()])
        couleurCoinN.append(dico2[couleurCoin[k].upper()])
   
   # On crée un variable qui compte le nombre de chiffres identique entre posiontCoinN et couleurCoinN
    count = 0
    for k in range(3):
        if positionCoinN[k] in couleurCoinN:
            count += 1
    # 4 cas
    # 1er cas : il n'y a auncun chiffre commun au deux valeur
    if count == 0:
        for k in range(2):
            cube.moveHoraire('d')
    # 2eme et 3eme cas : il y a 1 seul chiffre en commun
#    if count == 1:
        
        
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
            # Pour eviter le bug python
            truc = 1
            # Déplacer la face DOWN de telle sorte que le coin soit directement en dessous de son emplacement finale
        else:
            truc = 0
            # Ajouter cette position dans la liste des exceptions
                
                
    
        



def D_cross(cube):

	face=cube.L[6]

	if not face[0][1]==face[1][0]==face[1][2]==face[2][1]: #la croix n'est ps presente

		#cas des arretes opposees

		if face[0][1] == face[2][1] :
			mvt = "LBDB'D'L'"

		elif face[1][0] == face[1][2]:
			mvt = "BRDR'D'B'"

		#sinon cas des arretes ajacentes

		elif face[1][0]== face[0][1]:
			mvt = "BDRD'R'B'"

		elif face[1][0] == face[2][1]:
			mvt = "RDFD'F'R'"

		elif face[1][2] == face[0][1]:
			mvt = "LDBD'B'L'"

		elif face[1][2] == face[2][1]:
			mvt = "FDLD'L'F'"
        #sinon aucune presente
       else:
			mvt = "FDLD'L'F'LBDB'D'L'"

	#la croix est faite mais il faut que les arretes soient bien placees

	rearranger_croix(cube, False) #on re-arrange la croix

# Exemples :
cube = struct.Cube("OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG")
cube.afficheFaces()
print(locate(cube, 'URL',2, 'O'))
#cube.affichage()
    # Up + Left + Front + Right + Back + Down (+ : concaténation)

#Exemple CocoM
cube=struct.Cube()
print(cube.isX('L','G'))

