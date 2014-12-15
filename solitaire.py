import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
import options
from random import *
from fonctions_generales import *
import principale

############################################################################################
############################################################################################
############################################################################################

def random_jeu_sol(cartes_alea, nombre_paquets) :
    ##Crée le plateau de jeu, en fonction des cartes aléatoires
    ##et du nombre de paquets.
    nombre_cartes = len(cartes_alea)

    i = 0
    j = 0

    card = []
    line = []
    game = [] ##Variable de sortie

    ##TABLEAU
    ##On commence par créer les n colonnes du tableau principal.
    ##La première aura 1 carte, la deuxième 2, etc. On s'arrête
    ##lorsque la somme est supérieure à la moitié du nombre total
    ##de cartes.
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

    ##ARRIVÉE
    ##On ajoute ensuite les emplacements de l'arrivée, correspondant
    ##à 4 fois le nombre de paquets.
    for i in range(nombre_paquets*4) :
        game.append([])

    ##PIOCHE
    ##Enfin, on place le reste des cartes dans la pioche, et on
    ##rajoute une dernière liste correspondant à la pioche retournée.
    while j < int(len(cartes_alea)) :
        card.append(cartes_alea[j])
        card.append(1)
        line.append(card)
        card = []
        j = j+1
    game.append(line)
    game.append([])
    
    return(game)

############################################################################################
############################################################################################
############################################################################################

def taille_fenetre(game) :
    ##Définit la taille de la fenêtre en fonction de l'emplacement
    ##de la dernière colonne du tableau de jeu.
    for i in range(len(game)-2) :
        for j in range(len(game[i])) :
            ##On recherche uniquement les colonnes où au moins
            ##une carte est retournée au début du jeu.
            if game[i][j][1] == 0 :
                pass
            else :
                last_column = i*85+400

    return(last_column)

############################################################################################
############################################################################################
############################################################################################

def cardclick(mouse_coord, game, last_column, nombre_paquets) :
    ##Renvoie la carte sélectionnée, sa position en pixels, sa
    ##position dans game, et si on peut la retourner ou non.

    card_select = ""
    pos = []
    cardplace = []
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
            ##S'il n'y a aucune carte dans la colonne, alors on renvoie
            ##une carte vide.
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

############################################################################################
############################################################################################
############################################################################################

def record_list(liste) :
    ##Permet d'enregistrer le plateau de jeu au tour précédent.

    prov1 = []
    prov2 = []
    prov3 = []
    
    for i in range(len(liste)) :
        for j in range(len(liste[i])) :
            for k in range(len(liste[i][j])) :
                prov3.append(liste[i][j][k])
            prov2.append(prov3)
            prov3 = []
        prov1.append(prov2)
        prov2 = []

    return(prov1)
    
############################################################################################
############################################################################################
############################################################################################

def blitimages (fenetre, game, nombre_paquets, last_column, type_cartes, type_dos) :

    dos = pygame.image.load("images/classic/dos/" + type_dos + ".png")
    vide = pygame.image.load("images/carte_vide/V00.png")
    dico_images = images("images/" + type_cartes + "/cartes/")
        
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

    ##Affichage d'une carte vide s'il n'y a plus de cartes dans la pioche
    if game[-2] == [] :
        fenetre.blit(vide, (50,50))
    else :
        fenetre.blit(dos, (50,50))

############################################################################################
############################################################################################
############################################################################################

def solitaire(type_cartes, taille_jeu, nombre_paquets) :
    pygame.init()
    pygame.display.set_caption("MIASHS")

    ##Chargement des images
    fond = pygame.image.load("images/fond/fond.png")
    image_select1 = pygame.image.load("images/select.png") 
    image_select2 = pygame.image.load("images/select2.png")
    image_select_top = pygame.image.load("images/select_top.png")

    ##Définition du jeu
    nombre_cartes = int(taille_jeu/4)

    ##Règles d'empilement dans le tableau
    regles_jeu = [nombre_cartes, "start", "inf", "diff_color", "king", "solitaire"]

    ##Règles d'empilement dans l'arrivée
    regles_empile = [nombre_cartes, "start", "sup", "same_symbol", "ace", "solitaire"]

    ##Répertoire des cartes par défaut
    type_cartes = "classic"
    type_dos = "dos6"

    ##Génération d'un jeu aléatoire
    cartes_alea = generation_jeu_aleatoire("images/" + type_cartes + "/cartes/", nombre_cartes, nombre_paquets)

    ##Génération du plateau de jeu
    game = random_jeu_sol(cartes_alea, nombre_paquets)

    ##Création du dictionnaire d'images
    dico_images = images("images/" + type_cartes + "/cartes/")

    ##Création de la feneêtre de jeu
    last_column = taille_fenetre(game)
    fenetreX, fenetreY = last_column+150, 750
    fenetre = pygame.display.set_mode((fenetreX, fenetreY))
    fond = pygame.transform.scale(fond, (fenetreX, fenetreY))
    fenetre.blit(fond, (0,0))

    ##Création des variables de jeu
    card_select1 = "" ##Carte sélectionnée
    card_select2 = "" ##Carte comparée
    rectoverso = 0 ##Définit si l'on peut retourner une carte ou non
    tomove = []  ##Définit l'ensemble des cartes à déplacer
    cardplace1 = [] ##Définit l'emplacement dans game de la carte 1
    cardplace2 = [] ##Définit l'emplacement dans game de la carte 2
    selection = "" ##Définit l'icône sélectionnée dans la barre latérale
    save = [] ##Enregistrement du plateau de jeu au tour précédent

    ##Boucle de jeu
    while True:        
        for event in pygame.event.get():

            ##Récupération des coordonnées de la souris
            mouse_coord = pygame.mouse.get_pos()

            ##Affichage du fond
            fenetre.blit(fond,(0,0))
            
            ##Affichage du plateau de jeu
            blitimages (fenetre, game, nombre_paquets, last_column, type_cartes, type_dos)

            ##Évènement de fermeture
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            ##Affichage de la barre latérale
            selection = barre_laterale(fenetre, fenetreX, mouse_coord)
            
            ##Actualisation de la barre latérale
            if event.type == MOUSEMOTION :
                mouse_coord = pygame.mouse.get_pos()
                selection = barre_laterale(fenetre, fenetreX, mouse_coord)
            
            ##Gestion des clics
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                if selection == "menu" :
                    principale.main()
                if selection == "options" :
                    type_cartes, restart = options.options(fenetre, type_cartes, nombre_cartes*4, nombre_paquets, False)
                    if restart == True :
                        solitaire()
                if selection == "retour" :
                    if not save == [] :
                        game = record_list(save)
                        save = []
                    
                ##Clic dans la pioche retournée                
                if 50 < mouse_coord[0] < 125 and 50 < mouse_coord[1] < 163 :
                    save = record_list(game)
                    
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

                    card_select1 = ""
                    pos1 = []
                    cardplace1 = []
             
                ##Si aucune carte n'est sélectionnée                
                if card_select1 == "" :

                    ##Alors on peut sélectionner une carte
                    try :
                        card_select1, pos1, cardplace1, rectoverso = cardclick(mouse_coord, game, last_column, nombre_paquets)
                        ##On retourne la carte si c'est possible
                        if rectoverso == 1 :
                            game[cardplace1[0]][cardplace1[1]][1] = 1
                            card_select1 = ""
                            pos1 = []
                            cardplace1 = []
                            
                    except :
                        card_select1 = ""
                        pos1 = []
                        cardplace1 = []

                ##Si une carte est déjà sélectionnée
                else :
                    valid = False

                    ##On sélectionne une deuxième carte
                    card_select2, pos2, cardplace2, rectoverso = cardclick(mouse_coord, game, last_column, nombre_paquets)

                    ##On retourne la carte si c'est possible
                    if rectoverso == 1 :
                        try : 
                            game[cardplace2[0]][cardplace2[1]][1] = 1
                        except :
                            pass

                    try :
                        if len(game)-3-nombre_paquets*4 < cardplace2[0] < len(game)-2 :
                            valid = check_move(card_select1, card_select2, regles_empile)
                        else :
                            valid = check_move(card_select1, card_select2, regles_jeu)
                    except :
                        pass

                    ##Désélection de la carte si on clique dessus à nouveau
                    if card_select1 == card_select2 :
                        card_select1 = ""
                        card_select2 = ""
                        pos1 = []
                        pos2 = []
                        cardplace1 = []
                        cardplace2 = []

            ##Gestion du clic droit
            if event.type == MOUSEBUTTONDOWN and event.button == 3 :

                ##Sélection d'une carte
                try :
                    card_select1, pos1, cardplace1, rectoverso = cardclick(mouse_coord, game, last_column, nombre_paquets)
                except :
                    card_select1 = ""
                    pos1 = []
                    cardplace1 = []

                ##Vérification si un emplacement est disponible dans l'arrivée
                for i in range(nombre_paquets*4) :
                    try :
                        card_select2 = game[len(game)-2-nombre_paquets*4+i][-1][0]
                    except :
                        card_select2 = "V00.png"
                    cardplace2 = [len(game)-2-nombre_paquets*4+i, -1, 0]
                    pos2 = []
                    try :
                        valid = check_move(card_select1, card_select2, regles_empile)
                    except :
                        pass
                    if valid == True :
                        break

            ##Vérification de la validité du mouvement
            if not card_select1 == "" and not card_select2 == "" :
                        
                if valid == True and cardplace2[0] < len(game)-2 :
                    save = record_list(game)
                    tomove = game[cardplace1[0]][cardplace1[1]:]
                    tomove.reverse()
                    for i in range(len(tomove)) :
                        game[cardplace2[0]].append(tomove[-1])
                        tomove.pop()
                        game[cardplace1[0]].pop()
                    card_select1 = ""
                    cardplace1 = []
                    pos1 = []
                    valid = False

                ##Sinon, la deuxième carte devient la carte sélectionnée
                else :
                    card_select1 = card_select2
                    pos1 = pos2
                    cardplace1 = cardplace2
                    
                card_select2 = ""
                pos2 = []
                cardplace2 = []
                        
            ##Si la carte sélectionnée est une carte vide (dans l'arrivée), alors on ne sélectionne rien
            if card_select1 == "V00.png" :
                card_select1 = ""
                pos1 = []
                cardplace1 = []
                          
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

            ##Vérification de la fin de jeu
            try :
                win = 1
                for i in range(nombre_paquets*4) :
                    if not int(game[len(game)-2-nombre_paquets*4+i][-1][0][1:3]) == 13 :
                        win = 0
                if win == 1 :
                    print("Vous avez gagné !")
            except :
                pass
                           
            pygame.display.flip()      

