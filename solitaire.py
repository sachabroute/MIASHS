import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
from random import *
from ordre_valeurs import *

def random_jeu_sol(repertoire_cartes, regles, nombre_paquets) :
    generation_cartes(repertoire_cartes, regles, nombre_paquets)
    

def main() :
    pygame.init()
    pygame.display.set_caption("MIASHS")
    fenetre = pygame.display.set_mode((1175, 750))

    cartes_alea = generation_jeu_aleatoire("images/simpsons/cartes/", 13, 1)
    nombre_cartes = len(cartes_alea)

    longueur_paquet = 0
    i = 0
    game = []

    while longueur_paquet < len(cartes_alea)/2 :
        game.append(cartes_alea[longueur_paquet:longueur_paquet+i])
        longeur_paquet = longueur_paquet + i
        i = i+1
    print(game)
        
    
