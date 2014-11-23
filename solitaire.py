import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
from random import *
from ordre_valeurs import *

def random_jeu_sol(cartes_alea) :
    nombre_cartes = len(cartes_alea)

    i = 0
    j = 0
    game = []
    rectoverso = []
    line = []

    while j < int(len(cartes_alea)/2) :      
        i = i+1
        j = j+i
        game.append(cartes_alea[j:j+i])
    game.append(cartes_alea[j:])

    for i in range(len(game)-1) :
        for j in range(len(game[i])-1) :
            line.append(0)
        line.append(1)
        rectoverso.append(line)
        line = []
    for i in range(len(game[-1])) :
        line.append(0)
    rectoverso.append(line)
    
    return(game, rectoverso)    

def main() :
    pygame.init()
    pygame.display.set_caption("MIASHS")
    fenetre = pygame.display.set_mode((1175, 750))

    cartes_alea = generation_jeu_aleatoire("images/simpsons/cartes/", 13, 1)
    game, rectoverso = random_jeu_sol(cartes_alea)

    liste_images = images("images/simpsons/cartes/") 

