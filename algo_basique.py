# algo_basique.py in branch structureDeDonnee
# -*- coding: utf-8 -*-

import numpy as np

import utils as struct

from PIL import Image, ImageDraw

# posface, poscube, posligne
# face, colonne, ligne
locaz =[ 
[[0,0,0],[1,0,0],[4,2,0]],
[[0,1,0],[4,1,0]],
[[0,2,0],[4,0,0],[3,2,0]],
[[0,0,1],[1,1,0]],
[[0,1,1]], #Milieu UP
[[0,2,0],[3,1,0]],
[[0,0,2],[1,2,0],[2,0,0]],
[[0,1,2],[2,1,0]],
[[0,2,2],[2,2,0],[3,0,0]],
[[5,0,0],[2,0,2],[1,2,2]],
[[5,1,0],[2,1,2]],
[[5,2,0],[2,2,2],[3,0,2]],
[[5,0,1],[1,1,2]],
[[5,1,1]], #Milieu DOWN
[[5,2,1],[3,1,2]],
[[5,0,2],[1,0,2],[4,2,2]],
[[5,1,2],[4,1,2]],
[[5,2,2],[3,2,2],[4,0,2]],
[[1,0,1],[4,2,1]],
[[1,2,1],[2,0,1]],
[[2,2,1],[3,0,1]],
[[3,2,1],[4,0,1]],
[[1,1,1]], #Milieu LEFT
[[2,1,1]], #Milieu FRONT
[[3,1,1]], #Milieu RIGHT
[[4,1,1]], #Milieu BACK
]

def link(posface, poscube, posligne):
    """
    La fonction link donne l'integralité des faces liés à une face.
    """
    for i in range(0,len(locaz)):
        if [posface,poscube,posligne] in locaz[i]:
            r = [] # On recompose une liste pour mettre la face du petit cube qui va en argument de la fonction en premier sur le résultat.
            r.append([posface,poscube,posligne])
            for j in range(0,len(locaz[i])):
                if locaz[i][j] != [posface,poscube,posligne]:
                    r.append(locaz[i][j])
            return r
            
def locate(cube, ignoreface, type, color, ignorepos = [], dico={'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
    """
    La fonction locate recherche la position de la face d'un cube ainsi que les faces liées au petit cube.
    cube: Objet cube
    ignoreface: String (exemple: 'URL' pour ignorer les faces Up Right Left dans la recherche.)
    type: 1 ou 2 (1: Coin 2: Arrête)
    color: La couleur qu'on veut rechercher
    ignorepos: Une liste qui va contenir des positions de faces, la fonction va ignorer ces faces dans la recherche.
    Return [(pos white, face white), (pos link1, face link1), [(pos link1, face link1) si type 1]]
    """
    ignoreList = [] # On ignore les faces dans la liste.
    for i in range(0,len(ignoreface)): # On va correspondre la lettre avec le numéro de la face.
        idFace = dico[ignoreface[i].upper()]
        ignoreList.append(idFace)
    j = 0
    i = 0
    while j < 6: # On va loop pour faire l'intégralité du cube
        while i < 3 and not(j in ignoreList): # On va bien sur ignorer les faces sur la ignore list.
            if type == 1:  # Type 1 : Coin
                if 0 in (np.where(cube.L[j][i] == color)[0]) and not([j,0,i] in ignorepos):
                    return link(j,0,i)
                elif 2 in (np.where(cube.L[j][i] == color)[0]) and not([j,2,i] in ignorepos):
                    return link(j,2,i)
            elif type == 2:  # Type 2 : Arrête
                if (1 in (np.where(cube.L[j][i] == color)[0]) and not([j,1,i] in ignorepos) and not i == 1 ):
                    return link(j,1,i)
                elif i == 1:
                    if 0 in (np.where(cube.L[j][i] == color)[0]) and not([j,0,i] in ignorepos):
                        return link(j,0,i)
                    elif 2 in (np.where(cube.L[j][i] == color)[0]) and not([j,2,i] in ignorepos):
                        return link(j,2,i)
            i = i+1
        k = 0
        i = 0
        j = j+1
    return None

def place_croix(placement, mvt):
    r = []
    if mvt == 'U':
        for i in range(0,4):
            j = (i+1)%4
            r.append(placement[j])
        return r
    elif mvt == "U'":
        for i in range(0,4):
            r.append(placement[(3+i)%4])
        return r

def cross(cube, face):
    """
    On va fabriquer la croix.
    cube: Objet cube
    face: string qui va definir la face où on fait la croix
    return: String (suite de mvts)
    On modifie notre objet cube au passage.
    De façon optimale, en général, il faudrait atteindre la croix en 6 coups (Je sais pas par quel miracle http://www.cubezone.be/crossstudy.html).
    """
    # On le fait en 4 étapes, on positionne successivement les différentes arrêtes.
    # Première étape, regarde si c'est deja terminé.
    mvt = ""
    dico={'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}
    cubetemp = cube
    c = False
    loca_arretes = []
    placement_croix = {'L':0, 'R':0, 'F':0, 'B':0} 
    # Il s'agit de savoir dans quel sens est tourné la croix.
    nombre_arrete_place = 0
    # while c == False:
    #     result = locate(cube, '',2, 'W', loca_arretes)
    #     if result == None:
    #         c = True
    #     else:
    #         # posface, poscube, posligne
    #         # face, colonne, ligne
    #         #if result[0][0] == 0 and result[0][1] == 1: 'L':1, 'F':2, 'R':3, 'B':4
    #         for j in range(0,len(result)):
    #             if not(result[j][0] == 0):
    #                 loca_arretes.append(result[j])
    #             else:
    #                 if result[j][1] == 0:
    #                     placement_croix['L'] = 1 
    #                 elif result[j][1] == 2:
    #                     placement_croix['R'] = 1 
    #                 elif result[j][1] == 1 and result[j][2] == 2:
    #                     placement_croix['F'] = 1 
    #                 elif result[j][1] == 1 and result[j][2] == 0:
    #                     placement_croix['B'] = 1 
    # place_liste = [placement_croix['L'], placement_croix['F'], placement_croix['R'], placement_croix['B']]
    # ignoreArrete = []
    place_liste = [0,0,0,0]
    # Deuxieme etape, on place succecivement les arrêtes.
    prochaine_arrete_a_placer = locate(cube, 'U',2, 'W') # On localise la prochaine arrête.
    while 1 == 1:
        cubetemp = struct.Cube(cube.chaine)
        if mvt != "":
            suitemvt(cubetemp,mvt)
            
            # cubetemp.afficheFaces()
        # stt = str(mvt) + "test.png"
        # affichage(cubetemp, stt)    
        prochaine_arrete_a_placer = locate(cubetemp, 'U',2, 'W') # On localise la prochaine arrête.
        if prochaine_arrete_a_placer != None:
            None
        else:
            return mvt

        # En fonction de où elle se trouve et de ce qui est présent sur la croix on tourne la croix
        # On a differents cas ensuite
        # Cas 1: http://rubiks3x3.com/algorithm/?moves=FrdRff&fields=nwnwwwnwnnonnonnnnngnngnnnnnrnnrnnnnnbnnbnnnnnnnnnnnnn&initrevmove=FrdRFF
        #     

        # Cas 2: http://rubiks3x3.com/algorithm/?moves=frdRff&fields=nwnwwwnwnnonnonnnnngnngnnnnnrnnrnnnnnbnnbnnnnnnnnnnnnn&initrevmove=frdRFF
        #
        # Cas 3: http://rubiks3x3.com/algorithm/?moves=rdRff&fields=nwnwwwnwnnonnonnnnngnngnnnnnrnnrnnnnnbnnbnnnnnnnnnnnnn&initrevmove=rdRff
        #
        # Cas 4: Quand la face est orienté sur la face opposé, il suffit de bien positionner la croix et faire tourner.
        #
        # print(prochaine_arrete_a_placer)
        # print(place_liste)
        # print(mvt)
        if prochaine_arrete_a_placer[0][0] == 1: # LEFT
            if prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 2:
                #BAS
                while place_liste[0]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "L"
                while place_liste[3]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "B'"
                place_liste[3]=1
            elif prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 0:
                #HAUT
                mvt = mvt + "L'"
                while place_liste[3]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "B'"
                place_liste[3]=1
            elif prochaine_arrete_a_placer[0][1] == 0:
                #GAUCHE
                while place_liste[3]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "B'"
                place_liste[3] = 1
            elif prochaine_arrete_a_placer[0][1] == 2:
                #DROIT
                while place_liste[1]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "F"
                place_liste[1] = 1

        elif prochaine_arrete_a_placer[0][0] == 2: # FRONT
            if prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 2:
                #BAS
                while place_liste[1]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "F"
                while place_liste[0]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "R'"
                place_liste[0]=1
            elif prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 0:
                #HAUT
                mvt = mvt + "F'"
                while place_liste[0]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "L'"
                place_liste[0]=1
            elif prochaine_arrete_a_placer[0][1] == 0:
                #GAUCHE
                while place_liste[0]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "L'"
                place_liste[0] = 1
            elif prochaine_arrete_a_placer[0][1] == 2:
                #DROIT
                while place_liste[2]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "R"
                place_liste[2] = 1

        elif prochaine_arrete_a_placer[0][0] == 3: # RIGHT
            if prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 2:
                #BAS
                while place_liste[2]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "R"
                while place_liste[1]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "F'"
                place_liste[1]=1
            elif prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 0:
                #HAUT
                mvt = mvt + "R'"
                while place_liste[1]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "F'"
                place_liste[1]=1
            elif prochaine_arrete_a_placer[0][1] == 0:
                #GAUCHE
                while place_liste[1]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "F'"
                place_liste[1]=1
            elif prochaine_arrete_a_placer[0][1] == 2:
                #DROIT
                while place_liste[3]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "B"
                place_liste[3] = 1

        elif prochaine_arrete_a_placer[0][0] == 4: # BACK
            if prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 2:
                #BAS
                while place_liste[3]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "B"
                while place_liste[2]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "R'"
                place_liste[2]=1
            elif prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 0:
                #HAUT
                mvt = mvt + "B'"
                while place_liste[2]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "R'"
                place_liste[2]=1
            elif prochaine_arrete_a_placer[0][1] == 0:
                #GAUCHE
                while place_liste[2]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "R'"
                place_liste[2]=1
            elif prochaine_arrete_a_placer[0][1] == 2:
                #DROIT
                while place_liste[0]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "L"
                place_liste[0] = 1

        elif prochaine_arrete_a_placer[0][0] == 5: # DOWN
            if prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 2:
                #BAS
                while place_liste[3]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "B2"
                place_liste[3]=1
            elif prochaine_arrete_a_placer[0][1] == 1 and prochaine_arrete_a_placer[0][2] == 0:
                #HAUT
                while place_liste[1]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "F2"
                place_liste[1]=1
            elif prochaine_arrete_a_placer[0][1] == 0:
                #GAUCHE
                while place_liste[0]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "L2"
                place_liste[0]=1
            elif prochaine_arrete_a_placer[0][1] == 2:
                #DROIT
                while place_liste[2]==1:
                    mvt = mvt + "U"
                    place_liste = place_croix(place_liste, 'U')
                mvt = mvt + "R2"
                place_liste[2]=1  

    return mvt


def affichage(cube, save):
    """
    Fonction qui va creer une image PNG qui donne l'affichage du cube.
    cube: objet cube
    save: string (Nom du fichier de sauvegarde (ne pas preciser extension))
    """
    img = Image.new( 'RGB', (255,255), (220,220,220)) # create a new black image
    dico={'O':"orange", 'R':"red", 'W':"white", 'G':"green", 'B':"blue", 'Y':"yellow"}
    draw = ImageDraw.Draw(img)
    # draw.line((0, 0) + img.size, fill=128)
    # draw.line((0, img.size[1], img.size[0], 0), fill=128)
    draw.rectangle([(28,78),(76,126)],(211,211,211))
    draw.rectangle([(78,78),(126,126)],(211,211,211))
    draw.rectangle([(128,78),(176,126)],(211,211,211))
    draw.rectangle([(178,78),(226,126)],(211,211,211))

    draw.rectangle([(78,28),(126,76)],(211,211,211))
    draw.rectangle([(78,128),(126,176)],(211,211,211))

    # UP
    draw.rectangle([(78,28),(94,44)], dico[cube.L[0][0][0]])
    draw.rectangle([(94,28),(110,44)], dico[cube.L[0][0][1]])
    draw.rectangle([(110,28),(126,44)], dico[cube.L[0][0][2]])

    draw.rectangle([(78,44),(94,60)], dico[cube.L[0][1][0]])
    draw.rectangle([(94,44),(110,60)], dico[cube.L[0][1][1]])
    draw.rectangle([(110,44),(126,60)], dico[cube.L[0][1][2]])

    draw.rectangle([(78,60),(94,76)], dico[cube.L[0][2][0]])
    draw.rectangle([(94,60),(110,76)], dico[cube.L[0][2][1]])
    draw.rectangle([(110,60),(126,76)], dico[cube.L[0][2][2]])
    # FRONT
    draw.rectangle([(78,78),(94,94)], dico[cube.L[2][0][0]])
    draw.rectangle([(94,78),(110,94)], dico[cube.L[2][0][1]])
    draw.rectangle([(110,78),(126,94)], dico[cube.L[2][0][2]])

    draw.rectangle([(78,94),(94,110)], dico[cube.L[2][1][0]])
    draw.rectangle([(94,94),(110,110)], dico[cube.L[2][1][1]])
    draw.rectangle([(110,94),(126,110)], dico[cube.L[2][1][2]])

    draw.rectangle([(78,110),(94,126)], dico[cube.L[2][2][0]])
    draw.rectangle([(94,110),(110,126)], dico[cube.L[2][2][1]])
    draw.rectangle([(110,110),(126,126)], dico[cube.L[2][2][2]])
    # DOWN
    draw.rectangle([(78,128),(94,144)], dico[cube.L[5][0][0]])
    draw.rectangle([(94,128),(110,144)], dico[cube.L[5][0][1]])
    draw.rectangle([(110,128),(126,144)], dico[cube.L[5][0][2]])

    draw.rectangle([(78,144),(94,160)], dico[cube.L[5][1][0]])
    draw.rectangle([(94,144),(110,160)], dico[cube.L[5][1][1]])
    draw.rectangle([(110,144),(126,160)], dico[cube.L[5][1][2]])

    draw.rectangle([(78,160),(94,176)], dico[cube.L[5][2][0]])
    draw.rectangle([(94,160),(110,176)], dico[cube.L[5][2][1]])
    draw.rectangle([(110,160),(126,176)], dico[cube.L[5][2][2]])
    # LEFT
    draw.rectangle([(28,78),(44,94)], dico[cube.L[1][0][0]])
    draw.rectangle([(44,78),(60,94)], dico[cube.L[1][0][1]])
    draw.rectangle([(60,78),(76,94)], dico[cube.L[1][0][2]])

    draw.rectangle([(28,94),(44,110)], dico[cube.L[1][1][0]])
    draw.rectangle([(44,94),(60,110)], dico[cube.L[1][1][1]])
    draw.rectangle([(60,94),(76,110)], dico[cube.L[1][1][2]])

    draw.rectangle([(28,110),(44,126)], dico[cube.L[1][2][0]])
    draw.rectangle([(44,110),(60,126)], dico[cube.L[1][2][1]])
    draw.rectangle([(60,110),(76,126)], dico[cube.L[1][2][2]])
    # RIGHT
    draw.rectangle([(128,78),(144,94)], dico[cube.L[3][0][0]])
    draw.rectangle([(144,78),(160,94)], dico[cube.L[3][0][1]])
    draw.rectangle([(160,78),(176,94)], dico[cube.L[3][0][2]])

    draw.rectangle([(128,94),(144,110)], dico[cube.L[3][1][0]])
    draw.rectangle([(144,94),(160,110)], dico[cube.L[3][1][1]])
    draw.rectangle([(160,94),(176,110)], dico[cube.L[3][1][2]])

    draw.rectangle([(128,110),(144,126)], dico[cube.L[3][2][0]])
    draw.rectangle([(144,110),(160,126)], dico[cube.L[3][2][1]])
    draw.rectangle([(160,110),(176,126)], dico[cube.L[3][2][2]])
    # BACK
    draw.rectangle([(178,78),(194,94)], dico[cube.L[4][0][0]])
    draw.rectangle([(194,78),(210,94)], dico[cube.L[4][0][1]])
    draw.rectangle([(210,78),(226,94)], dico[cube.L[4][0][2]])

    draw.rectangle([(178,94),(194,110)], dico[cube.L[4][1][0]])
    draw.rectangle([(194,94),(210,110)], dico[cube.L[4][1][1]])
    draw.rectangle([(210,94),(226,110)], dico[cube.L[4][1][2]])

    draw.rectangle([(178,110),(194,126)], dico[cube.L[4][2][0]])
    draw.rectangle([(194,110),(210,126)], dico[cube.L[4][2][1]])
    draw.rectangle([(210,110),(226,126)], dico[cube.L[4][2][2]])

    #img.show()
    img.save(save+".png", "PNG")
    
def suitemvt(cube, mvt):
    #mvt : chaine
    #cube :declass cube
    for i in range(len(mvt)):
        if mvt[i] in ['U', 'L', 'F', 'R', 'B', 'D']:

            if i<len(mvt)-1 and mvt[i+1]=="'" :
                cube.moveAntiHoraire(mvt[i]) #Nom de la fonction a changer si besoin
            else:
                cube.moveHoraire(mvt[i])
        elif mvt[i] == str(2):
            cube.moveHoraire(mvt[i-1])

def rearranger_croix(cube, faceup):
    '''
    Permet de mettre les arrete de la croix des face up et down a leur place
    La croix est déjà formée de base
    faceup : boleen pour differencier face up et down (croix de différente manière)
    '''
    mvt = ""
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
            mvt = mvt + face


    if nbplace != 4: #si les 4 sont bien placé, rien a faire
        ## Cas 2 arrêtes en place côte à côte
        if enplace[3] == enplace[0] == 1:
            if faceup: #c'est plus opimise niveau mouvment si on considere differremment les face up  et down
                mvt ="RU'R'UR"
            else:
                mvt ="FD2F'D'FD'F'D'"
        elif enplace[0]==enplace[1] == 1:
            if faceup:
                mvt = "BU'B'UB"
            else:
                mvt="RD2R'D'RD'R'D'"
        elif enplace[1]==enplace[2] == 1:
            if faceup:
                mvt = "LU'L'UL"
            else:
                mvt = "BD2B'D'BD'B'D'"
        elif enplace[2]==enplace[3]==1:
            if faceup:
                mvt = "FU'F'UF"
            else:
                mvt = "LD2L'D'LD'L'D'"

        ##Cas 2 arrêtes en place en face
        elif enplace[0]==enplace[2]==1:
            if faceup:
                mvt = "FU2F'U2F"
            else:
                mvt = "LD2L'D'LD'L'FD2F'D'FD'F'D'"
        elif enplace[1]==enplace[3]==1:
            if faceup:
                mvt = "LU2L'U2L"
            else:
                mvt = "FD2F'D'FD'D'LD2L'D'LD'L'D'"
    return mvt
        # suitemvt(cube,mvt)

def idChangeCornerDown(positionCoin, couleurCoin):
    '''
    Change les références du coin lorsque la face DOWN a été tourné dans le sens horaire 
    '''
    L=["LFD","FRD","RBD","BLD"]
    
    # On recherche le coin dans la liste
    # i : curseur mot dans la liste
    # rg : rang du mot trouvé
    i=0   
    while i < 4:        
                # k : rang de la lettre dans le mot
                k = 0
                count = 0
                while k < 3:
                    if positionCoin[k] not in L[i]:
                        k=3
                        i+=1
                    else:
                        count+=1
                        k+=1
                    
                    if count == 3:
                        rg = i
                        i+=1
                 
                

    # On opère le changement de référence
    # Si le mot n'est pas le dernier de la liste
    positionCoinInter=L[rg]
    if rg < 4:        
        positionCoinFinal=L[rg+1]
    #Sinon
    if rg == 4:
        positionCoinFinal=L[0]
    # On pose couleurCoinInter pour pouvoir placer les couleur à l'emplacement voulu
    couleurCoinInter=[0,0,0]
    for m in range(3):
        for n in range(3):
            if positionCoin[m]==positionCoinInter[n]:
                couleurCoinInter[n]=couleurCoin[m]
                
    # Concaténation de la couleur finale du coin           
    couleurCoinFinal = ""    
    for j in range(3):
        couleurCoinFinal+=couleurCoinInter[j]
        
        
    return [positionCoinFinal,couleurCoinFinal]      
            
def cornerInPlace(cube, positionCoin, couleurCoin, dico={'U':0, 'L':1, 'F':2, 'R':3, 'B':4, 'D':5}):
    '''
    Si le coin n'est pas situé en dessous de son emplacement final, la fonction tourne la face DOWN
    du cube de tel sorte qu'il soit alors à la bonne place. Si le coin est déjà bien placé, elle retourne True.
    
    positionCoin : chaine de 3 caractère ( Ex : "LFD" ) 
    couleurCoin  : chaine de 3 caractère ( Ex : "WBR" )
    
    Dans l'exemple : sur la face Left le coin est White, sur la face Front le coin est Bleu, etc...
    
    renvoie la positionCoin et couleurCoin  du coin bien placé
    '''         
    dico2={cube.L[0][1][1]:0, cube.L[1][1][1]:1, cube.L[2][1][1]:2, cube.L[3][1][1]:3, cube.L[4][1][1]:4, cube.L[5][1][1]:5}
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
    # 3 cas
    # 1er cas : il n'y a aucun chiffre commun au deux valeur
    if count == 0:
        for k in range(2):            
            suitemvt(cube, "D")
            affichage(cube, "ex"+"end_3")
            if k == 0:
                ref = idChangeCornerDown(positionCoin,couleurCoin)
            else:
                return idChangeCornerDown(ref[0], ref[1]), "D2"
            
    # 2eme cas : il y a 1 seul chiffre en commun et on refait appelle à la fonction de façon récursif
    elif count == 1:
        suitemvt(cube,"D")
        affichage(cube, "ex"+"end_3")
        ref = idChangeCornerDown(positionCoin,couleurCoin)
        return cornerInPlace(cube, ref[0], ref[1])[0], cornerInPlace(cube, ref[0], ref[1])[1]+"D"
    # 3ème cas : le coin est à la bonne place
    # on ne fait rien
    elif count == 2:
        affichage(cube, "ex"+"end_3")
        return [positionCoin, couleurCoin], ""
        
def bienOriente(cube, positionCoin, couleurCoin):
    '''
    positionCoin et couleurCoin sont des chaines de 3 caractères  (EX : "FRU" / "BWR" => mal orienté | "FRU" / "RBW" => bien orienté)
    
    Détermine si le coin est bien orienté
    Renvoie True ou False
    '''
    verif = [('U',cube.L[0][1][1]),('L',cube.L[1][1][1]),('F',cube.L[2][1][1]),('R',cube.L[3][1][1]),('B',cube.L[4][1][1]),('D',cube.L[5][1][1])]
    count=0
    for k in range(3):
        for i in range(6):
            if positionCoin[k]==verif[i][0] and couleurCoin[k]==verif[i][1]:
                count+=1
    if count==3:
        return True
    else:
        return False
                
#def remplacement(cube,positionCoin,coord,mvt):
#    # Tant que le coin positionCoin n'est pas bien orientée
#    refCoin=positionCoin
#    refCouleur=coord
#    while not bienOriente(refCoin, refCouleur):
#        # Faire la suite de mouvement
#        suitemvt(cube,mvt)
#        refCouleur=coord
#        affichage(cube, "ex"+"end_3")        
        
def wFace_1st_crown(cube, dico3={0:'U', 1:'L', 2:'F', 3:'R', 4:'B', 5:'D'}):
    '''
    Cette fonction termine la face blanche et fait la 1ère couronne du cube    
    '''
    # Liste des exceptions (coin a ne pas parcourir) ici correspond au facette des coins supérieur ou facette appartenant à UP
    exception = [[1,0,0],[1,2,0],[2,0,0],[2,2,0],[3,0,0],[3,2,0],[4,0,0],[4,2,0]]
    # Tant que la face blanche n'est pas totalement blanche
    while not cube.isFull('U','W'):
                
        
        # Chercher un coin avec une facette blanche sur toutes autres face hormis la face UP
        corner = locate(cube,'U',1,'W', exception)
        
        # S'il reste des facettes blanches sur des coins inférieur
        if corner != None:
        
            
            # Si le coin trouvé est sur l'étage du bas (3ème couronne + face DOWN) et qu'il n'a pas déjà été pointé
            rowCorner = corner[0][2]
            if rowCorner == 2 or corner[0][0] == 5:            
            
                # Détermination de la couleur "lettrée" du coin
                couleurCoin=""
                for k in range(3):
                    couleurCoin+=cube.L[corner[k][0]][corner[k][2]][corner[k][1]]
                    
                # Détermination de la position "lettrée" du coin
                positionCoin=""
                for k in range(3):
                    positionCoin+=dico3[corner[k][0]]
                
                # Déplacer la face DOWN de telle sorte que le coin soit directement en dessous de son emplacement finale
                ref = cornerInPlace(cube, positionCoin, couleurCoin)
                
                # Si le coin est en FRD
                if  ("F" in ref[0][0]) and ("R" in ref[0][0]) and ("D" in ref[0][0]):
                    # Tant que le coin positionCoin n'est pas bien orientée
                    while not bienOriente(cube, "UFR", cube.L[0][2][2]+cube.L[2][0][2]+cube.L[3][0][0]):
                        # Faire la suite de mouvement
                        suitemvt(cube,"R'D'RD")
                        affichage(cube, "ex"+"end_3") 
                # Si le coin est en LFD
                if  ("L" in ref[0][0]) and ("F" in ref[0][0]) and ("D" in ref[0][0]):
                    # Tant que le coin positionCoin n'est pas bien orientée
                    while not bienOriente(cube, "LFU", cube.L[1][0][2]+cube.L[2][0][0]+cube.L[0][2][0]):
                        # Faire la suite de mouvement
                        suitemvt(cube,"F'D'FD")
                        affichage(cube, "ex"+"end_3")                    
                # Si le coin est en BLD
                if  ("B" in ref[0][0]) and ("L" in ref[0][0]) and ("D" in ref[0][0]):
                    # Tant que le coin positionCoin n'est pas bien orientée
                    while not bienOriente(cube, "BLU", cube.L[4][0][2]+cube.L[1][0][0]+cube.L[0][0][0]):
                        # Faire la suite de mouvement
                        suitemvt(cube,"L'D'LD")
                        affichage(cube, "ex"+"end_3")                    
                # Si le coin est en RBD
                if  ("R" in ref[0][0]) and ("B" in ref[0][0]) and ("D" in ref[0][0]):
                    # Tant que le coin positionCoin n'est pas bien orientée
                    while not bienOriente(cube, "RBU", cube.L[3][0][2]+cube.L[4][0][0]+cube.L[0][0][2]):
                        # Faire la suite de mouvement
                        suitemvt(cube,"B'D'BD")
                        affichage(cube, "ex"+"end_3")
                    
        ## Il est possible que la face blanche ne soit pas entièrement remplie et que le nombre de coin
        ## de la face DOWN ayant une facette blanche soient épuisé
        else:
            corner_final = locate(cube,'U',1,'W')
            
            # Détermination de la couleur "lettrée" du coin
            couleurCoin=""
            for k in range(3):
                couleurCoin+=cube.L[corner_final[k][0]][corner_final[k][2]][corner_final[k][1]]
                
            # Détermination de la position "lettrée" du coin
            positionCoin=""
            for k in range(3):
                positionCoin+=dico3[corner_final[k][0]]
        
            # Si le coin est en UFR
            if  ("U" in positionCoin) and ("F" in positionCoin) and ("R" in positionCoin):
#                remplacement(cube,"UFR",[0,2,2]+[2,2,0]+[3,0,0],"R'D'RD")
                # Tant que le coin positionCoin n'est pas bien orientée
                while not bienOriente(cube, "UFR", cube.L[0][2][2]+cube.L[2][0][2]+cube.L[3][0][0]):
                    # Faire la suite de mouvement
                    suitemvt(cube,"R'D'RD")
                    affichage(cube, "ex"+"end_3")                   
            # Si le coin est en LFU
            if  ("L" in positionCoin) and ("F" in positionCoin) and ("U" in positionCoin):
#                remplacement(cube,"LFU",[1,2,0]+[2,0,0]+[0,0,2],"F'D'FD")
                # Tant que le coin positionCoin n'est pas bien orientée
                while not bienOriente(cube, "LFU", cube.L[1][0][2]+cube.L[2][0][0]+cube.L[0][2][0]):
                    # Faire la suite de mouvement
                    suitemvt(cube,"F'D'FD")
                    affichage(cube, "ex"+"end_3")
            # Si le coin est en BLU
            if  ("B" in positionCoin) and ("L" in positionCoin) and ("U" in positionCoin):
#                remplacement(cube,"BLU",[4,2,0]+[1,0,0]+[0,0,0],"L'D'LD")
                # Tant que le coin positionCoin n'est pas bien orientée
                while not bienOriente(cube, "BLU", cube.L[4][0][2]+cube.L[1][0][0]+cube.L[0][0][0]):
                    # Faire la suite de mouvement
                    suitemvt(cube,"L'D'LD")
                    affichage(cube, "ex"+"end_3")
            # Si le coin est en RBU
            if  ("R" in positionCoin) and ("B" in positionCoin) and ("U" in positionCoin):
#                remplacement(cube,"RBU",[3,2,0]+[4,0,0]+[0,2,0],"B'D'BD")
                # Tant que le coin positionCoin n'est pas bien orientée
                while not bienOriente(cube, "RBU", cube.L[3][0][2]+cube.L[4][0][0]+cube.L[0][0][2]):
                    # Faire la suite de mouvement
                    suitemvt(cube,"B'D'BD")
                    affichage(cube, "ex"+"end_3")

    
def D_cross(cube):

    '''
    Cette fonction permet de faire la croix sur la derniere face
    Il y a trois cas differrent:
        on a une moitie de croix qui forme une ligne (arretes opposees)
        on a une moite de croix qui 'encadre' un coin (arretes adjacentes)
        aucune vignette de la croix n'est présente
    Pour chacun des cas, il y a une séquence qui fait la croix.
    Pour les 2 1er cas, il y a différentes disposition des cube, la séquence reste la meme mais pas avec le meme referentiel de face.
    ensuite on rearrange la croix, pour que les arretes jaune soit avec leur 2eme couleur.
    rearranger_croix est adapté pour ça
    '''
    
    face=cube.L[5]

    if not face[0][1]==face[1][0]==face[1][2]==face[2][1]: #la croix n'est ps presente

        # cas des arretes opposees
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

        suitemvt(cube, mvt)
	#la croix est faite mais il faut que les arretes soient bien placees

    rearranger_croix(cube, False) #on re-arrange la croix

def place_D_corner(cube):
    #couleurs des faces
    colors = {'U' : cube.L[0][1][1], 'L' : cube.L[1][1][1], 'F' : cube.L[2][1][1], 'R': cube.L[3][1][1],
    'B' : cube.L[4][1][1], 'D' : cube.L[5][1][1]}
    # les coins actuels de la face D associé aux 3 couleurs
    corners = {'FLD': cube.L[1][2][2] + cube.L[2][2][0] + cube.L[5][0][0],
    'FRD' : cube.L[2][2][2] + cube.L[3][2][0] + cube.L[5][0][2],
    'BRD' : cube.L[3][2][2] + cube.L[4][2][0] + cube.L[5][2][2],
    'BLD' : cube.L[1][2][0] + cube.L[4][2][2] + cube.L[5][2][0]}

    enplace = []

    for i in corners: #on cherche les coin bien placés
        if (colors[i[0]] in corners[i]) and  (colors[i[1]] in corners[i]) and (colors[i[2]] in corners[i]):
            enplace.append(i)


    #on a forcement 0,1 ou 4 coin bien placés
    if len(enplace) != 4: #si les 4 ne sont pas tous bien placés
        if len(enplace) == 0:
            mvt = "LD'R'DL'D'RD"
            #si aucun n'est bien placé, on fait une des 4 combinaison de mouvenments.
            #il y aura alors au moins un bien placé.
            suitemvt(cube,mvt)
            place_D_corner(cube)
        else: #il y a alors forcément un coin bien placé

            cornerP = enplace[0]
            # En fonction de la position des coins, il faut determiner dans quel sens les faire changer de position.
            #Seul celui en place ne bougera pas.
            if cornerP != 'FRD':
                if cornerP != 'BRD':
                    if colors['F'] in corners['BRD'] and colors['R'] in corners['BRD']:
                        sensH = False
                    else:
                        sensH = True
                elif cornerP != 'FLD':
                    if colors['F'] in corners['FLD'] and colors['R'] in corners['FLD']:
                        sensH = True
                    else:
                        sensH = False
            else:
                if colors['B'] in corners['BLD'] and colors['R'] in corners['BLD']:
                    sensH = False
                else:
                    sensH = True

            #Les cas differents en fonction de la position du coin place et le sens dans lequel les faires bouger
            if cornerP=='FLD':
                if sensH:
                    mvt="R'DLD'RDL'D'"

                else:
                    mvt ="BD'F'DB'D'FD"

            elif cornerP =='FRD':
                if sensH:
                    mvt="B'DFD'BDF'D'"
                else:
                    mvt="'LD'R'DL'D'RD"

            elif cornerP =='BRD':
                if sensH:
                    mvt="L'DRD'LRD'"
                else:
                    mvt="FD'B'DF'D'BD"

            else:
                if sensH:
                    mvt="F'DBD'FDB'D'"
                else:
                    mvt="RD'L'DR'D'LD"

            suitemvt(cube,mvt)

def orient_D_corner(cube):

    Face={0:'U', 1:'L', 2:'F', 3:'R', 4:'B', 5:'D'}
    oppFace={1:'R',2:'B',3:'L',4:'F'}

    C= cube.L[5][1][1]

    for i in range(1,5):
        if cube.L[i][2][0] == cube.L[i][2][2] == C:
            F=Face[i]
            Fo = oppFace[i]
            mvt = F + "D2" + F +"'D'"+F +"D'"+F+"'"+Fo+"'D2" + Fo+"D"+Fo+"'D"+Fo
            
            suitemvt(cube,mvt)
    

    while not cube.isFull('D',C):

        if cube.L[5][0][0] == cube.L[5][0][2] == cube.L[2][1][1]:
            mvt = "DF2D'F'DF'D'U'F2UFU'FU"
        elif cube.L[5][2][2] == cube.L[5][0][2] == cube.L[3][1][1]:
            mvt = "DR2D'R'DR'D'U'R2URU'RU"
        elif cube.L[5][2][2] == cube.L[5][2][0] == cube.L[4][1][1]:
            mvt = "DB2D'B'DB'D'U'B2UBU'BU"
        elif cube.L[5][0][0] == cube.L[5][2][0] == cube.L[1][1][1]:
            mvt = "DL2D'L'DL'D'U'L2ULU'LU"
        suitemvt(cube,mvt)


def solve(cube_c54) :
    """
    Résoud une configuration de cube et renvoie la suite des mouvements à réaliser.
    
    :param cube_c54: string d'un cube au format 54
    """
    cube = struct.Cube(cube_c54)
    # process de résolution (à compléter)
    return cube.solution


## AU MOMENT DE MERGER, PENSER A ENLEVER LES EXEMPLES !! ##
# Sinon, une pythonnerie fait qu'ils seront exécutés au chargement de ce fichier (import alg_basique)..
# Pour en garder une trace, mettez les dans poqb.py ;) (et n'oubliez pas de faire import alg_basique)


# Exemples :
# cube = struct.Cube("OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG")
# cube.afficheFaces()
#print(locate(cube, 'U',1, 'W', [[4, 2, 1], [1, 0, 1],[1, 0, 2], [5, 0, 2], [4, 2, 2]]))
# print(cross(cube,"W"))
#suitemvt(cube,"LB'FR'U")
#affichage(cube, "lp.png")

#example = ["YBBRWORRGRBWGGWOBOWYBGOOYGOWRYRBOGWYBBWBWYOYYOWRGYRRGG",
#"WRROWYGBYOWOYRBRBGYGBYOWGGOGRBWBGOWBOYWBRRGBGYORRYYWOW",
#"WRWWWRWOYRROGWOBBRBGGGOBYGGYRRYBWBOYOYOBORYWRGOWGYBYBG",
#"OWOBWGRRBBWGYGRYYYGGWBORWGYBRRYBRGWOYORGOBRYWBBWOYGOOW",
#"BBOWWGWBGRRGROWOWBYYWWOOYGOWRRBBBGGBYGYOGOBRYROGRYYRYW",
#"RYYOWGGORYYOYWBWYBRRGWOGOGYBRWGBBGOOYRRGGOBWWBBWBYRORW",
#"WYGWWYBGYRROWRBRBOYRGOOYGGYORWGBGYRYBWWBOGOBROBRBYWGOW",
#"WRRGWBWYBORGRGWROGYBBOOOYGYBRWRBGYGRBBWGOOGROYWOWYWBYY",
#"ROOWWBYYWBROBGBOOGWWYGOBYGBRRGWBOBYWRWGYYRYGWGBORYORRG",
#"YBWWWOWYBORRBBYOYGRRGWOBOGWBRWOBGWGGRYBYYOBGOYGRRYRGOW",
#"GRRBWOORRYOBYYGYYYBGOYOWBGYGRWOBBOOGWGRWROBRGRWBGYWWBW",
#"BGBYWWRWWOOGYGOGROWYYOORGGRYRYBBBROBYBYOWGWRBRWGGYOWBR",
#"RWBGWGBBRBYYORGYOWRBYWORGGRYRYBBGOBOBOGWWOGRGWYROYOWWY",
#"RYGWWOORGBRYGYYRGRWGYOORGGBYRGWBWBBOBOYBRGOBWWYOOYBRWW",
#"OYGGWRBYRGYOWOYBYYRBYOOWGGBWRWRBWRBOYOGOGRGBBBGWOYRWRW",
#"RYGWWWRROWOWGGYGBWOGBGGBYRWRBRYOWYOYRRWOGYBORBBBBYOGYO"]
#
#for i in range(0,len(example)):
#    cu = struct.Cube(example[i])
#    affichage(cu, str(i)+" debut")
#    a = cross(cu,"W")
#    suitemvt(cu,a)
#    affichage(cu, str(i)+" end_1_" + a)
#    b = rearranger_croix(cu, "U")
#    suitemvt(cu,b)
#    affichage(cu, str(i)+" end_2_" + a + b)
#    wFace_1st_crown(cu)
#    affichage(cu, "ex"+"end_3")   

## Test CocoM
#ex = "RYGWWWRROWOWGGYGBWOGBGGBYRWRBRYOWYOYRRWOGYBORBBBBYOGYO"
ex2 = "RWYWWWOWWBGBYRBOBRGOYRGYRROBBBYOGRBRGYGOGOGYBWGWRYOWOY"
ex3 = "BWYWWWBWBOORYGWRRYOBGOORYGBRRBYBYYYWGGOBRWROROOWGYGGBG"
cu = struct.Cube(ex3)
affichage(cu, "ex3_"+" debut")
#a = cross(cu,"W")
#suitemvt(cu,a)
#affichage(cu, "ex_"+" end_1_" + a)
#b = rearranger_croix(cu, "U")
#suitemvt(cu,b)
#affichage(cu, "ex_"+" end_2_" + a + b)
wFace_1st_crown(cu)
affichage(cu, "ex3_"+"end_3")



    # Up + Left + Front + Right + Back + Down (+ : concaténation)

#print(idChangeCornerDown("DRF","GWO"))

#print(bienOriente("FRU","RBW"))