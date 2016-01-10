# example.py
# -*- coding: utf-8 -*-

import numpy as np
import random
import utils as struct

from PIL import Image, ImageDraw


def Cube_to_chain(cube):
    i = 0
    j = 0
    r = ""
    while j < 3: # On va loop pour faire l'intégralité du cube
        while i < 3:
            if j == 0:
                for k in range(0,3):
                    r = r + str(cube.L[j][i][k]) 
            elif j == 1:
                for k in range(0,3):
                    r = r + str(cube.L[j][i][k]) 
                for k in range(0,3):
                    r = r + str(cube.L[j+1][i][k]) 
                for k in range(0,3):
                    r = r + str(cube.L[j+2][i][k]) 
                for k in range(0,3):
                    r = r + str(cube.L[j+3][i][k]) 
            elif j == 2:
                for k in range(0,3):
                    r = r + str(cube.L[j+3][i][k]) 
            i = i+1
        i = 0
        j = j+1
    return r

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

def example_generate(chaine, nombreseq, nombregenerations):
    """
    chaine: Chaine VALIDE du RBK
    nombreseq: Nombre de mouvement à faire par generations
    nombregenerations: Nombre de générations de chaines
    """
    cube = struct.Cube(chaine)
    dico = ['U','L','F','R','B','D']
    i = 0
    while i < nombregenerations:
        r = ""
        for j in range(0,nombreseq):
            r = r+dico[random.randint(0,5)]
            suitemvt(cube,r)
        print(Cube_to_chain(cube))
        i = i+1
    return True

example_generate("OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG", 8, 15)

