import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
from random import *
from fonctions_generales import *

def random_jeu_sol(cartes_alea, nombre_paquets) :
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

    for i in range(nombre_paquets*4) :
        game.append([])
        
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

def cardclick(mouse_coord, game, last_column, nombre_paquets) :

    card_select = ""
    pos = []
    game_column = len(game)-1
    rectoverso = 0

    ##Sélection d'une carte du tableau
    for i in range(int((last_column-400)/85)+1) :
        ##Sélection de la colonne
        if i*85+400 < mouse_coord[0] < i*85+475 :

            ##Sélection de la carte sur la colonne
            j = len(game[i])-1
            if j*25+213 < mouse_coord[1] < j*25+326 :
                card_select = game[i][-1][0]
                pos = [i*85+400, j*25+213]
                game_column = i
                if game[i][-1][1] == 0 :
                    rectoverso = 1

    ##Sélection d'une carte de la pioche                                
    if 135 < mouse_coord[0] < 210 and 50 < mouse_coord[1] < 163 :
        card_select = game[-1][-1][0]
        pos = [135, 50]

    ##Sélection d'une carte de l'arrivée
    if 50 < mouse_coord[1] < 163 :
        for i in range(nombre_paquets*4) :
            if last_column-i*85 < mouse_coord[0] < last_column+75-i*85 :
                game_column = len(game)-2-nombre_paquets*4+i
                try :
                    card_select = game[-2-nombre_paquets*4+i][-1][0]   
                except :
                    pass
                if card_select == "" :
                    card_select = "V00.png"
                else :
                    pass
                pos = [last_column-i*85, 50]

    return(card_select, pos, game_column, rectoverso)
    
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
    regles_jeu = [nombre_cartes, "start", "sup", "diff_color"]
    regles_empile = [nombre_cartes, "start", "inf", "same_color"]
    
    cartes_alea = generation_jeu_aleatoire("images/classic/cartes/", nombre_cartes, nombre_paquets)
    game = random_jeu_sol(cartes_alea, nombre_paquets)

    dico_images = images("images/classic/cartes/")
    last_column = taille_fenetre(game)
    fenetre = pygame.display.set_mode((last_column+125, 750))
    fenetre.blit(fond, (0,0))
    fenetre.blit(dos, (50,50))
    fenetre.blit(vide, (135,50))
    card_select1 = ""
    card_select2 = ""
    game_column1 = len(game)-1
    game_column2 = len(game)-1
    rectoverso = 0

    print(game)

    while True:        
        for event in pygame.event.get():

            ##Évènement de fermeture
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            ##Affichage du fond
                fenetre.blit(fond,(0,0))
                
            ##Affichage des cartes du jeu
            ##Affichage des cartes du tableau
            for i in range(len(game)-(2+nombre_paquets*4)) :
                for j in range(len(game[i])) :

                    ##Affichage du dos des cartes si elles sont verso
                    if game[i][j][1] == 0 :
                        fenetre.blit(dos, (i*85+400,j*25+213))

                    ##Affichage de la carte si elles sont recto
                    else :
                        fenetre.blit(dico_images[game[i][j][0]], (i*85+400,j*25+213))
                        last_column = i*85+400

            ##Affichage des cartes de l'arrivée
            ##Affichage des cartes vides
            for i in range(nombre_paquets*4) :
                fenetre.blit(vide, (last_column-(85*i),50))
                
            ##Affichage des cartes rangées
            for i in range(nombre_paquets*4) :
                for j in range(len(game[-3-i])) :
                    fenetre.blit(dico_images[game[-3-i][j][0]], (last_column-i*85,50))
            
            ##Gestion des clics
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :

                pos = []
                mouse_coord = pygame.mouse.get_pos()

                ##Clic dans la pioche                
                if 50 < mouse_coord[0] < 125 and 50 < mouse_coord[1] < 163 :

                    ##Gestion des paquets
                    ##Suppression d'une carte dans la pioche cachée et ajout d'une autre dans la pioche affichée
                    try :
                        game[-1].append(game[-2][-1])
                        game[-2].pop()
                    ##Sinon il n'y a plus de cartes dans la pioche cachée, la pioche affichée devient pioche cachée.
                    except :
                        game[-2] = game[-1]
                        game[-1] = []

                    ##Affichage d'une carte vide si la pioche cachée est vide
                    if game[-2] == [] :
                        fenetre.blit(vide, (50,50))

                    ##Affichage d'un dos s'il reste encore des cartes
                    else :
                        fenetre.blit(dos, (50,50))

                ##Si aucune carte n'est sélectionnée                
                if card_select1 == "" :

                    ##Alors on peut sélectionner une carte
                    try :
                        card_select1, pos1, game_column1, rectoverso = cardclick(mouse_coord, game, last_column, nombre_paquets)
                        if rectoverso == 1 :
                            game[game_column1][-1][1] = 1
                    except :
                        pass

                ##Si une carte est déjà sélectionnée
                else :
                    valid = False

                    ##On sélectionne une deuxième carte
                    card_select2, pos2, game_column2, rectoverso = cardclick(mouse_coord, game, last_column, nombre_paquets)
                    print(game_column2)
                    print(len(game)-2-nombre_paquets*4, len(game)-2)
                    if len(game)-2-nombre_paquets*4 < game_column2 < len(game)-2 :
                        valid = check_move(card_select1, card_select2, regles_empile)
                    else :
                        valid = check_move(card_select1, card_select2, regles_jeu)
                    
                    #try :
                        ##On vérifie si le mouvement est valide
                        #valid = check_move(card_select1, card_select2, regles)
                        #print(valid)
                    #except :
                        #pass

                    ##Si oui, le mouvement est validé
                    if valid == True :
                        game[game_column2].append(game[game_column1][-1])
                        game[game_column1].pop()
                        valid = False
                        card_select1 = ""
                        card_select2 = ""
                        pos1 = ""
                        pos2 = ""

                    ##Sinon, la deuxième carte devient la carte sélectionnée
                    else :
                        card_select1 = card_select2
                        pos1 = pos2
                        card_select2 = 0
                        pos2 = 0

                ##Si la carte sélectionnée est une carte vide (dans l'arrivée), alors on ne sélectionne rien
                if card_select1 == "V00.png" :
                    card_select1 = ""
                    pos1 = []
                    
            if event.type == KEYDOWN and event.key == K_q :
                print(card_select1, card_select2)

            ##On affiche la dernière carte de la pioche retournée
            try :
                fenetre.blit(dico_images[game[-1][-1][0]], (135,50))
            ##Sinon on affiche une carte vide
            except :
                fenetre.blit(vide, (135,50))

            ##Affichage des contours de sélection
            try :
                fenetre.blit(image_select1, (pos1[0], pos1[1]))
                fenetre.blit(image_select2, (pos2[0], pos2[1]))
            except :
                pass

            pygame.display.flip()

if __name__ == '__main__':
  main()            

    
            

