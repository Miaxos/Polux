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
[[5,2,2],[3,2,2],[4,1,2]],
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
                if 1 in (np.where(cube.L[j][i] == color)[0]) and not([j,1,i] in ignorepos):
                    return link(j,1,i)
            i = i+1
        i = 0
        j = j+1
    return None
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
    c = False
    loca_arretes = []
    placement_croix = [0,0,0,0] # [UP, RIGHT, LEFT, DOWN]
    # Il s'agit de savoir dans quel sens est tourné la croix.
    nombre_arrete_place = 0
    while c == False:
        result = locate(cube, 'RLBFD',2, 'W', loca_arretes)
        if result == None:
            c = True
        else:
            loca_arretes.append(append)
    nombre_arrete_place = len(loca_arretes)
    if nombre_arrete_place == 4:
        return mvt
    elif nombre_arrete_place == 0:
        # On doit donc en placer 4
        placement_croix = [0,0,0,0]
    else:
        #On met à jour placement_croix pour qu'il soit conforme au positinnement de la croix.
        None
    # Deuxieme etape, on place succecivement les arrêtes.
    while nombre_arrete_place < 4:
        prochaine_arrete_a_placer = locate(cube, 'U',2, 'W') # On localise la prochaine arrête.

        # En fonction de où elle se trouve et de ce qui est présent sur la croix on tourne la croix
        # On a differents cas ensuite
        # Cas 1: http://rubiks3x3.com/algorithm/?moves=FrdRff&fields=nwnwwwnwnnonnonnnnngnngnnnnnrnnrnnnnnbnnbnnnnnnnnnnnnn&initrevmove=FrdRFF
        # 
        if prochaine_arrete_a_placer[0][0] == 5:

        # Cas 2: http://rubiks3x3.com/algorithm/?moves=frdRff&fields=nwnwwwnwnnonnonnnnngnngnnnnnrnnrnnnnnbnnbnnnnnnnnnnnnn&initrevmove=frdRFF
        #
        # Cas 3: http://rubiks3x3.com/algorithm/?moves=rdRff&fields=nwnwwwnwnnonnonnnnngnngnnnnnrnnrnnnnnbnnbnnnnnnnnnnnnn&initrevmove=rdRff
        #
        # Cas 4: Quand la face est orienté sur la face opposé, il suffit de bien positionner la croix et faire tourner.
        #

            mvt_temps = ""
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
        suitemvt(cube,mvt)

def idChangeCornerDown(positionCoin, couleurCoin):
    '''
    Change les références du coin lorsque la face DOWN a été tourné dans le sens horaire 
    '''
    L=["LFD","FRD","RBD","BLD"]
    
    # On recherche le coin dans la liste
    # i : rang du mot dans la liste
    # rg : variable pour sortir de la boucle while
    i=0
    rg = 0
    while i < 4 and rg < 4:
            # k : rang de la lettre dans le mot
            k = 0
            while k < 3:
                if positionCoin[k] not in L[i]:
                    k=3
                    i+=1
                    rg+=1
                k+=1
            rg=4
    # On opère le changement de référence
    # Si le mot n'est pas le dernier de la liste
    positionCoinInter=L[i]
    if i < 4:        
        positionCoinFinal=L[i+1]
    #Sinon
    if i==4:
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
    # 1er cas : il n'y a aucun chiffre commun au deux valeur
    if count == 0:
        for k in range(2):
            suitemvt(cube,"D")
            if k == 0:
                ref = idChangeCornerDown(positionCoin,couleurCoin)
            else:
                return idChangeCornerDown(ref[0], ref[1])
            
    # 2eme cas : il y a 1 seul chiffre en commun et on refait appelle à la fonction de façon récursif
    elif count == 1:
        suitemvt(cube,"D")
        ref = idChangeCornerDown(positionCoin,couleurCoin)
        cornerInPlace(cube, ref[1], ref[2])
    # 3ème cas : le coin est à la bonne place
    # on ne fait rien
    elif count == 2:
        return [positionCoin, couleurCoin]
        
def bienOriente(positionCoin, couleurCoin):
    '''
    positionCoin et couleurCoin sont des chaines de 3 caractères  (EX : "FRU" / "WOG")
    
    Détermine si le coin est bien orienté
    Renvoie True ou False
    '''
    verif = [('U','W'),('L','G'),('F','R'),('R','B'),('B','O'),('D','Y')]
    count=0
    for k in range(3):
        for i in range(6):
            if positionCoin[k]==verif[i][0] and couleurCoin[k]==verif[i][1]:
                count+=1
    if count==3:
        return True
    else:
        return False
                
        
        
def wFace_1st_crown(cube, dico3={0:'U', 1:'L', 'F':2, 3:'R', 4:'B', 5:'D'}):
    '''
    Cette fonction termine la face blanche et fait la 1ère couronne du cube    
    '''
    # Liste des exceptions (coin a ne pas parcourir) ici correspond au facette des coins supérieur or facette appartenant à UP
    exception = [[1,0,0],[1,2,0],[2,0,0],[2,2,0],[3,0,0],[3,2,0],[4,0,0],[4,2,0]]
    # Tant que la face blanche n'est pas totalement blanche
    while not cube.isFull('U','W'):
                
        
        # Chercher un coin avec une facette blanche sur toutes autres face hormis la face UP
        corner = cube.locate('U',1,'W', exception)
        
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
                if  "F" and "R" and "D" in ref[0]:
                    # Tant que le coin UFR n'est pas bien orientée
                    refCoin="UFR"
                    refCouleur=[0,2,2]+[2,2,0]+[3,0,0]
                    while not bienOriente(refCoin, refCouleur):
                        # Faire le suite de mouvement
                        suitemvt(cube,"R'D'RD")                    
                # Si le coin est en LFD
                if  "L" and "F" and "D" in ref[0]:
                    # Tant que le coin LFU n'est pas bien orientée
                    refCoin="LFU"
                    refCouleur=[1,2,0]+[2,0,0]+[0,0,2]
                    while not bienOriente(refCoin, refCouleur):
                        # Faire le suite de mouvement
                        suitemvt(cube,"F'D'FD")
                # Si le coin est en BLD
                if  "B" and "L" and "D" in ref[0]:
                    # Tant que le coin BLU n'est pas bien orientée
                    refCoin="BLU"
                    refCouleur=[4,2,0]+[1,0,0]+[0,0,0]
                    while not bienOriente(refCoin, refCouleur):
                        # Faire le suite de mouvement
                        suitemvt(cube,"L'D'LD")
                # Si le coin est en RBD
                if  "R" and "B" and "D" in ref[0]:
                    # Tant que le coin RBU n'est pas bien orientée
                    refCoin="RBU"
                    refCouleur=[3,2,0]+[4,0,0]+[0,2,0]
                    while not bienOriente(refCoin, refCouleur):
                        # Faire le suite de mouvement
                        suitemvt(cube,"B'D'BD")
        ## Il est possible que la face blanche ne soit pas entièrement remplie et que le nombre de coin
        ## de la face DOWN ayant une facette blanche soient épuisé
        else:
            corner_final = cube.locate('U',1,'W')
            
            # Détermination de la couleur "lettrée" du coin
            couleurCoin=""
            for k in range(3):
                couleurCoin+=cube.L[corner_final[k][0]][corner_final[k][2]][corner_final[k][1]]
                
            # Détermination de la position "lettrée" du coin
            positionCoin=""
            for k in range(3):
                positionCoin+=dico3[corner_final[k][0]]
        
            # Si le coin est en UFR
            if  "F" and "R" and "U" in positionCoin:
                # Tant que le coin UFR n'est pas bien orientée
                refCoin="UFR"
                refCouleur=[0,2,2]+[2,2,0]+[3,0,0]
                while not bienOriente(refCoin, refCouleur):
                    # Faire le suite de mouvement
                    suitemvt(cube,"R'D'RD")                    
            # Si le coin est en LFU
            if  "L" and "F" and "U" in positionCoin:
                # Tant que le coin LFU n'est pas bien orientée
                refCoin="LFU"
                refCouleur=[1,2,0]+[2,0,0]+[0,0,2]
                while not bienOriente(refCoin, refCouleur):
                    # Faire le suite de mouvement
                    suitemvt(cube,"F'D'FD")
            # Si le coin est en BLU
            if  "B" and "L" and "U" in positionCoin:
                # Tant que le coin BLU n'est pas bien orientée
                refCoin="BLU"
                refCouleur=[4,2,0]+[1,0,0]+[0,0,0]
                while not bienOriente(refCoin, refCouleur):
                    # Faire le suite de mouvement
                    suitemvt(cube,"L'D'LD")
            # Si le coin est en RBU
            if  "R" and "B" and "U" in positionCoin:
                # Tant que le coin RBU n'est pas bien orientée
                refCoin="RBU"
                refCouleur=[3,2,0]+[4,0,0]+[0,2,0]
                while not bienOriente(refCoin, refCouleur):
                    # Faire le suite de mouvement
                    suitemvt(cube,"B'D'BD")
             
def D_cross(cube):
    
    face=cube.L[6]
    
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

    for i in corners: #on cherche les coins bien placés
        if colors[i[0]] + colors[i[1] + colors[i[2]] = corners[i]:
            enplace.append(i)


    #on a forcement 0,1 ou 4 coins bien placés
    if len(enplace) != 4: #si les 4 ne sont pas tous bien placés
        if len(enplace) == 0:
            mvt = "LD'R'DL'D'RD"
            #si aucun n'est bien placé, on fait une des 4 combinaison de mouvenments.
            #il y aura alors au moins un bien placé.
            suitemvt(cube,mvt)
            place_D_corner(cube)
        else: #il y a alors forcément un coin bien placé
            #4 cas différent
            if enplace[0]='FLD':
                mvt = "F'DBD'FDB'D'"

            elif enplace[0] ='FRD':
                mvt ="R'DLD'RDL'D'"

            elif enplace[0] ='BRD':
                mvt="B'DFD'BDF'D'"

            else:
                mvt="L'DRD'LDR'D'"

            suitemvt(cube,mvt)

# Exemples :
cube = struct.Cube("OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG")
cube.afficheFaces()
print(locate(cube, 'URL',1, 'O'))
affichage(cube, "test")
    # Up + Left + Front + Right + Back + Down (+ : concaténation)

#print(idChangeCornerDown("DRF","GWO"))

print(bienOriente("FRU","RBW"))