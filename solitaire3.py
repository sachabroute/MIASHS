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

    card = []
    line = []
    game = []

    while j < int(len(cartes_alea)/2) : 
        for k in range(j,j+i) :
            card.append(cartes_alea[k])
            card.append(0)
            line.append(card)
            card = []
        card.append(cartes_alea[j+i])
        card.append(1)
        line.append(card)
        game.append(line)
        i = i+1
        j = j+i
        card = []
        line = []

    while j < int(len(cartes_alea)) :
        card.append(cartes_alea[j])
        card.append(0)
        line.append(card)
        card = []
        j = j+1
    game.append(line)
    game.append([])
    
    return(game)

def taille_fenetre(game) :
    for i in range(len(game)-2) :
        for j in range(len(game[i])) :
            if game[i][j][1] == 0 :
                pass
            else :
                last_column = i*85+400

    return(last_column)

def cardclick(mouse_coord, game, last_column) :
    for i in range(int((last_column-400)/85)+1) :
        if i*85+400 < mouse_coord[0] < i*85+475 :
            j = len(game[i])-1
            if j*25+213 < mouse_coord[1] < j*25+326 :
                card_select = game[i][-1][0]
                pos = [i*85+400, j*25+213]
                                
    if 135 < mouse_coord[0] < 210 and 50 < mouse_coord[1] < 163 :
        card_select = game[-1][-1][0]
        pos = [135, 50]

    return(card_select, pos)
    
def main() :
    pygame.init()
    pygame.display.set_caption("MIASHS")
    fenetre = pygame.display.set_mode((1175, 750))
    fond = pygame.image.load("images/fond/fond.png")
    dos = pygame.image.load("images/classic/dos/dos.png")
    vide = pygame.image.load("images/carte_vide/V00.png")
    image_select1 = pygame.image.load("images/select.png")
    image_select2 = pygame.image.load("images/select2.png")
    nombre_cartes = 13
    nombre_paquets = 1
    regles = [nombre_cartes, "start", "sup", "diff_color"]
    
    cartes_alea = generation_jeu_aleatoire("images/classic/cartes/", nombre_cartes, nombre_paquets)
    game = random_jeu_sol(cartes_alea)

    dico_images = images("images/classic/cartes/")
    last_column = taille_fenetre(game)
    fenetre = pygame.display.set_mode((last_column+125, 750))
    fenetre.blit(fond, (0,0))
    fenetre.blit(dos, (50,50))
    fenetre.blit(vide, (135,50))
    phase = 1

    while True:        
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            for i in range(len(game)-2) :
                for j in range(len(game[i])) :
                    if game[i][j][1] == 0 :
                        fenetre.blit(dos, (i*85+400,j*25+213))
                    else :
                        fenetre.blit(dico_images[game[i][-1][0]], (i*85+400,j*25+213))
                        last_column = i*85+400
            
            for i in range(nombre_paquets*4) :
                fenetre.blit(vide, (last_column-(85*i),50))

            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                card_select = ""
                pos = []
                mouse_coord = pygame.mouse.get_pos()
                if 50 < mouse_coord[0] < 125 and 50 < mouse_coord[1] < 163 :
                    try :
                        game[-1].append(game[-2][-1])
                        game[-2].pop()
                    except :
                        game[-2] = game[-1]
                        game[-1] = []                       
                    if game[-2] == [] :
                        fenetre.blit(vide, (50,50))
                    else :
                        fenetre.blit(dos, (50,50))

                if phase == 1 :
                    try :
                        card_select1, pos1 = cardclick(mouse_coord, game, last_column)
                        phase = 2
                    except :
                        pass

                if phase == 2 :
                    card_select2, pos2 = cardclick(mouse_coord, game, last_column)
                    valid = check_move(card_select1, card_select2, regles)
                    if valid == True :
                        print("Valid")
                    phase = 1

            try :
                fenetre.blit(dico_images[game[-1][-1][0]], (135,50))
            except :
                fenetre.blit(vide, (135,50))
            try :
                fenetre.blit(image_select1, (pos1[0], pos1[1]))
                fenetre.blit(image_select2, (pos2[0], pos2[1]))
            except :
                pass
            
                    
                    #phase = 2
                #if phase == 2 : 
                    #card_select2, pos = cardclick(mouse_coord, game, last_column)

            pygame.display.flip()
            

if __name__ == '__main__':
  main()            

    
            

