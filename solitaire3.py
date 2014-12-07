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
        card.append(1)
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
    cardplace = [0, 0, 0]
    rectoverso = 0

    ##Sélection d'une carte du tableau
    for i in range(int((last_column-400)/85)+1) :
        ##Sélection de la colonne
        if i*85+400 < mouse_coord[0] < i*85+475 :
            ##Sélection de la carte sur la colonne
            for j in range(len(game[i])) :
                if j*25+213 < mouse_coord[1] < j*25+326 and game[i][j][1] == 1 :
                    card_select = game[i][j][0]
                    cardplace = [i, j, 0]
                    pos = [i*85+400, j*25+213]
                if game[i][-1][1] == 0 :
                    rectoverso = 1
                    cardplace = [i, j, 0]
            if len(game[i]) == 0 :
                card_select = "V00.png"
                cardplace = [i, 0, 0]

    ##Sélection d'une carte de la pioche                                
    if 135 < mouse_coord[0] < 210 and 50 < mouse_coord[1] < 163 :
        cardplace = [len(game)-1, len(game[-1])-1, 0]
        card_select = game[-1][-1][0]
        pos = [135, 50]

    ##Sélection d'une carte de l'arrivée
    if 50 < mouse_coord[1] < 163 :
        for i in range(nombre_paquets*4) :
            if last_column-i*85 < mouse_coord[0] < last_column+75-i*85 :
                cardplace = [len(game)-3-i, len(game[-3-i])-1, 0]
                try :
                    card_select = game[-3-i][-1][0]   
                except :
                    pass
                if card_select == "" :
                    card_select = "V00.png"
                else :
                    pass
                pos = [last_column-i*85, 50]

    return(card_select, pos, cardplace, rectoverso)
    
def main() :
    pygame.init()
    pygame.display.set_caption("MIASHS")
    fenetre = pygame.display.set_mode((1175, 750))
    fond = pygame.image.load("images/fond/fond.png")
    dos = pygame.image.load("images/classic/dos/dos4.png")
    vide = pygame.image.load("images/carte_vide/V00.png")
    image_select1 = pygame.image.load("images/select.png")
    image_select2 = pygame.image.load("images/select2.png")
    image_select_top = pygame.image.load("images/select_top.png")
    nombre_cartes = 13
    nombre_paquets = 3
    regles_jeu = [nombre_cartes, "start", "sup", "diff_color", "king"]
    regles_empile = [nombre_cartes, "start", "inf", "same_symbol", "ace"]
    
    cartes_alea = generation_jeu_aleatoire("images/classic/cartes/", nombre_cartes, nombre_paquets)
    game = random_jeu_sol(cartes_alea, nombre_paquets)

    dico_images = images("images/classic/cartes/")
    last_column = taille_fenetre(game)
    fenetre = pygame.display.set_mode((last_column+125, 750))
    fond = pygame.transform.scale(fond, (last_column+125, last_column+125*750//1175))
    fenetre.blit(fond, (0,0))

    card_select1 = ""
    card_select2 = ""
    rectoverso = 0
    tomove = []

    while True:        
        for event in pygame.event.get():

            verify_if_win = []

            ##Évènement de fermeture
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            ##Affichage du fond
                fenetre.blit(fond,(0,0))
                
            ##Affichage des cartes du jeu
            ##Affichage des cartes du tableau
            for i in range(len(game)-(2+nombre_paquets*4)) :        
                
                ##Affichage d'une carte vide s'il n'y a plus de carte
                if game[i] == [] :
                    fenetre.blit(vide, (i*85+400,213))
                        
                for j in range(len(game[i])) :                    
                    ##Affichage du dos des cartes si elles sont verso
                    if game[i][j][1] == 0 :
                        fenetre.blit(dos, (i*85+400,j*25+213))

                    ##Affichage de la carte si elles sont recto
                    else :
                        fenetre.blit(dico_images[game[i][j][0]], (i*85+400,j*25+213))          

            ##Affichage des cartes de l'arrivée
            ##Affichage des cartes vides
            for i in range(nombre_paquets*4) :
                fenetre.blit(vide, (last_column-(85*i),50))
                
            ##Affichage des cartes rangées
            for i in range(nombre_paquets*4) :
                for j in range(len(game[-3-i])) :
                    fenetre.blit(dico_images[game[-3-i][j][0]], (last_column-i*85,50))
                    
            ##On affiche la dernière carte de la pioche retournée
            try :
                fenetre.blit(dico_images[game[-1][-1][0]], (135,50))
                
            ##Sinon on affiche une carte vide
            except :
                fenetre.blit(vide, (135,50))

            if game[-2] == [] :
                fenetre.blit(vide, (50,50))
            else :
                fenetre.blit(dos, (50,50))
            
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
                        game[-1].reverse()
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
                        card_select1, pos1, cardplace1, rectoverso = cardclick(mouse_coord, game, last_column, nombre_paquets)
                        if rectoverso == 1 :
                            game[cardplace1[0]][cardplace1[1]][1] = 1
                    except :
                        pass

                ##Si une carte est déjà sélectionnée
                else :
                    valid = False

                    ##On sélectionne une deuxième carte
                    card_select2, pos2, cardplace2, rectoverso = cardclick(mouse_coord, game, last_column, nombre_paquets)
                    if len(game)-3-nombre_paquets*4 < cardplace2[0] < len(game)-2 :
                        try :
                            valid = check_move(card_select1, card_select2, regles_empile)
                        except :
                            pass
                    else :
                        try :
                            valid = check_move(card_select1, card_select2, regles_jeu)
                        except :
                            pass

                    ##Si oui, le mouvement est validé
                    if valid == True :
                        tomove = game[cardplace1[0]][cardplace1[1]:]
                        tomove.reverse()
                        for i in range(len(tomove)) :
                            game[cardplace2[0]].append(tomove[-1])
                            tomove.pop()
                            game[cardplace1[0]].pop()
                        valid = False
                        card_select1 = ""
                        card_select2 = ""
                        pos1 = []
                        pos2 = []

                    ##Sinon, la deuxième carte devient la carte sélectionnée
                    else :
                        card_select1 = card_select2
                        pos1 = pos2
                        card_select2 = 0
                        pos2 = []
                        
                ##Si la carte sélectionnée est une carte vide (dans l'arrivée), alors on ne sélectionne rien
                if card_select1 == "V00.png" :
                    card_select1 = ""
                    pos1 = []
                    
            if event.type == KEYDOWN and event.key == K_q :
                print(card_select1, card_select2)
                print(cardplace1, cardplace2)
            if event.type == KEYDOWN and event.key == K_g :
                print("Tableau, ligne 1 :", game[0])
                print("Tableau, ligne 2 :", game[1])
                print("Tableau, ligne 3 :", game[2])
                print("Tableau, ligne 4 :", game[3])
                print("Tableau, ligne 5 :", game[4])
                print("Tableau, ligne 6 :", game[5])
                print("Tableau, ligne 7 :", game[6])
                print("/n")
                print("Tableau, arrivée 1 :", game[7])
                print("Tableau, arrivée 1 :", game[8])
                print("Tableau, arrivée 1 :", game[9])
                print("Tableau, arrivée 1 :", game[10])
                print("/n")
                print("Pioche couverte :", game[11])
                print("Pioche retournée :", game[12])
            if event.type == KEYDOWN and event.key == K_h :
                print(hello)
     
            ##Affichage des contours de sélection
            try :
                if cardplace1[1] == len(game[cardplace1[0]])-1 or cardplace[0] == len(game)-2 :
                    fenetre.blit(image_select1, (pos1[0], pos1[1]))
            except :
                pass
            try :
                if not cardplace1[1] == len(game[cardplace1[0]])-1 or cardplace[0] == len(game)-2 :
                    fenetre.blit(image_select_top, (pos1[0], pos1[1]))
                fenetre.blit(image_select2, (pos2[0], pos2[1]))
            except :
                pass

            try :
                for i in range(nombre_paquets*4) :
                    verify_if_win.append(int(game[len(game)-2-nombre_paquets*4+i][-1][0][1:3]))
                if sum(verify_if_win) == 52*nombre_paquets :
                    print("Vous avez gagné !")
            except :
                pass
                
                           
            pygame.display.flip()

            fenetre.blit(fond,(0,0))


if __name__ == '__main__':
  main()            

    
            

