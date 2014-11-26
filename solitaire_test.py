import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
from random import *
from fonctions_generales import *

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

def affichage_jeu(nombre_paquets, cartes_alea, rectoverso) :

    dos = pygame.image.load("images/simpsons/dos/dos.png")
    vide = pygame.image.load("images/carte_vide/V00.png")
    
    for i in range(len(game)-1) :
        for j in range(len(game[i])) :
            if rectoverso[i][j] == 0 :
                fond.blit(dos, (i*85+300,j*25+213))
            else :
                fond.blit(dico_images[cartes_alea[i]], (i*85+300,j*25+213))
                last_column = i*85+300

    fond.blit(dos, (50,50))
    fond.blit(vide, (135,50))

    for i in range(nombre_paquets*4) :
        fond.blit(vide, (last_column-(85*i),50))

def main() :
    pygame.init()
    pygame.display.set_caption("MIASHS")
    fenetre = pygame.display.set_mode((1175, 750))
    fond = pygame.image.load("images/fond/fond.png")

    nombre_cartes = 13
    nombre_paquets = 1
    
    cartes_alea = generation_jeu_aleatoire("images/simpsons/cartes/", nombre_cartes, nombre_paquets)
    game, rectoverso = random_jeu_sol(cartes_alea)

    dico_images = images("images/simpsons/cartes/")
    print(dico_images)

    while True:        
        for event in pygame.event.get():
            fenetre.blit(fond, (0,0))

            pygame.display.flip()

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            affichage_jeu(nombre_paquets, cartes_alea, rectoverso)

if __name__ == '__main__':
  main()            

    
            

