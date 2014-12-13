import pygame
from pygame.locals import *
import sys
import os
import time
from random import *
import game_options



def cheat_ordonne(shuffled, lignes, colonnes):
    ordered = [[],[],[],[]]
    indice_vide = 0
    for y in range(lignes):
        for x in range(colonnes + 1):
            if shuffled[y][x][0] == "C":
                ordered[0].append(shuffled[y][x])
            elif shuffled[y][x][0] == "D":
                ordered[1].append(shuffled[y][x])
            elif shuffled[y][x][0] == "H":
                ordered[2].append(shuffled[y][x])
            elif shuffled[y][x][0] == "S":
                ordered[3].append(shuffled[y][x])
            elif shuffled[y][x][0] == "V":
                ordered[indice_vide].append(shuffled[y][x])
                indice_vide += 1


                
    ordered[0].sort()
    ordered[1].sort()
    ordered[2].sort()
    ordered[3].sort()
    
    return(ordered)


def ordre_valeurs(nombre_cartes, place_as):
    ##Renvoie automatiquement une liste d'ordre des valeurs, selon le nombre de
    ##cartes dans les règles. Fonctionne pour nombre_cartes = 7, 8, 13, 14 et 16 :
    ##Jeu de 28 cartes (4*7) : 7, 8, 9, 10, J, Q, K
    ##Jeu de 32 cartes (4*8) : 1, 7, 8, 9, 10, J, Q, K
    ##Jeu de 52 cartes (4*13) : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
    ##Jeu de 56 cartes (4*14) : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, C, Q, K
    ##Jeu de 64 cartes (4*16) : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, J, C, Q, K
    ##La variable place_as permet de définir si le 1 doit se trouver au début ou
    ##à la fin du paquet.

    ordre_valeurs_cartes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 11, 14, 12, 13]
    ordre_priorite_cartes = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 14, 15, 16]
    ordre_selon_regles = []

    ordre_priorite_cartes = ordre_priorite_cartes[0:nombre_cartes]

    for i in range(len(ordre_valeurs_cartes)) :
        if ordre_valeurs_cartes[i] in ordre_priorite_cartes :
            ordre_selon_regles.append(ordre_valeurs_cartes[i])

    if 1 in ordre_selon_regles and place_as == "end" :
        ordre_selon_regles.insert(nombre_cartes-1, ordre_selon_regles.pop(0))
        
    return(ordre_selon_regles)


def chargement_images(type_cartes, regles):

    ordre = ordre_valeurs(regles, "start")

    ##Chargement des cartes
    liste_images_brutes = os.listdir("images/" + type_cartes + "/cartes/") ##Insère toutes les images du répertoire dans une liste
    liste_images_regles = [] ##Nouvelle liste qui contiendra uniquement les images de jeu

    ##Boucle supprimant les cartes cavalier si égal à 13
    for i in range(len(liste_images_brutes)) :
        cardsplit = liste_images_brutes[i] #On prend du caractère [1] au caractère [2] pour avoir le numéro de carte.
        cardnumber = cardsplit[1:3]
        if int(cardnumber) in ordre : ##Si ce numéro est inférieur au nombre dans règles, alors on append, sinon rien.
            liste_images_regles.append(liste_images_brutes[i])

    ##Fin du chargement des images
    nombre_cartes = int(len(liste_images_regles)) ##Définit le nombre de cartes à partir de la taille de la liste
    
    return(liste_images_regles, nombre_cartes)


def chargement_dico(type_cartes, regles):

    ##chargement des cartes
    liste_images_regles, nombre_cartes = chargement_images(type_cartes, regles)
    
    cartes = {} ## initialisation biblioteque vide
    
    for i in range(nombre_cartes):
        indice = liste_images_regles[i].split(".")[0] ## correspond au nom de chaque carte. on split pour enlever le '.png', on se retrouve avec 'C01', 'C02', etc...
        cartes["%s" %(indice)] = pygame.image.load("images/" + type_cartes + "/cartes/"+liste_images_regles[i]).convert_alpha()
    #### end load images (wouaaah c'est super court t'as vu!??)

    return(cartes)

def rajoute_carte_vide(cartes):
    cartes["V00"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
    return(cartes)


def napoleon(type_cartes, taille_jeu):
    pygame.init()
    pygame.display.set_caption("MIASHS")

    ##Définition des règles
    regles = int(taille_jeu / 4)
    fenetreX, fenetreY = (200+(regles+1)*80, 750)
    fenetre = pygame.display.set_mode((fenetreX, fenetreY))

    ##Chargement des images
    fond = pygame.image.load("images/fond/fond.png")
    fond = pygame.transform.scale(fond, (fenetreX, fenetreY))

    options = pygame.image.load("images/options/rouage.png")
    options_select = pygame.image.load("images/options/rouage_select.png")

    ##chargement des cartes
    liste_images_regles, nombre_cartes = chargement_images(type_cartes, regles)    

    lignes = 4
    colonnes = int(nombre_cartes / lignes)

    cartes = chargement_dico(type_cartes, regles)


    ## creation d'une liste de base, et melange de cartes
    liste_cartes = [name for name in cartes] ## prends chaque nom de cartes dans la biblioteque

    ## rajout de cartes vides a la fin des listes.
    cartes = rajoute_carte_vide(cartes)
    
    for i in range(lignes):
        liste_cartes.append("V00")

    shuffle(liste_cartes)
    shuffled = [liste_cartes[x:x + colonnes + 1] for x in range(0, len(liste_cartes), colonnes + 1)] ## cree une liste deux dimensions (lignes * colonnes) avec comme valeur les valeurs de liste_cartes
    
    ## rajout de cartes vides a la fin des listes.
##    cartes["V00"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
##    for i in range(lignes): ## on rajoute la carte vide à la fin de chaque ligne!
##        shuffled[i].append("V00") ## On la rajoute ici parce que si on la rajoutais avant, on aurais une carte vide qq part dans le tableau!


########## TEST select transparence
    select1 = pygame.image.load("images/select.png").convert_alpha()
    select2 = pygame.image.load("images/select2.png").convert_alpha()

##########
                

    mouseX, tableauY = (-1,-1)
    select_depart = False ## variable si la carte de depart a été selectionnée
    coord_depart = (-1,-1)
    select_dest = False ## variable si la carte de destination a été selectionnée
    coord_dest = (-1,-1)
    game_started = False ## devient true quand l'utilisateur commence a jouer! (utilise pour les options)

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:

                ## conversion coordonnées brutes en coordonnées tableau
                tableauX, tableauY = (mouseX - 30) // 80, (mouseY - 30) // 118
                if select_depart == False and 0 <= tableauX < colonnes + 1 and 0 <= tableauY < lignes and shuffled[tableauY][tableauX] != "V00": ## pour la carte de depart
                    coord_depart = tableauX, tableauY
                    select_depart = True
                ## si l'utilisateur click sur une carte au lieu du vide en deuxieme choix
                elif select_dest == False and 0 <= tableauX < colonnes + 1 and 0 <= tableauY < lignes and shuffled[tableauY][tableauX] != "V00":
                    coord_depart = tableauX, tableauY
                    select_depart = True
                elif select_dest == False and 0 <= tableauX < colonnes + 1 and 0 <= tableauY < lignes and shuffled[tableauY][tableauX] == "V00": ## pour la position de destination
                    coord_dest = tableauX, tableauY
                    select_dest = True
                elif fenetreX - 50 <= mouseX <= fenetreX - 20 and 15 <= mouseY <= 45:
                    type_cartes, taille_jeu, restart = game_options.options(fenetre, type_cartes, taille_jeu, game_started)
                    if restart:
                        napoleon(type_cartes, taille_jeu)
                    cartes = chargement_dico(type_cartes, regles)
                    cartes = rajoute_carte_vide(cartes) 

            if event.type == KEYDOWN:
                if event.key == K_o:
                    shuffled = cheat_ordonne(shuffled, lignes, colonnes)
                    time.sleep(0.2)


        ## affiche fond
        fenetre.blit(fond, (0,0))

        ## affiche rouage options
        fenetre.blit(options, (fenetreX - 50, 15))
        ## affiche rouage selectionne
        if fenetreX - 50 <= mouseX <= fenetreX - 20 and 15 <= mouseY <= 45:
            fenetre.blit(options_select, (fenetreX - 50, 15))
        
        ## affiche cartes
        for y in range(lignes):
            for x in range(colonnes + 1): # + 1 pour rajouter la carte vide à la fin de chaque ligne
                fenetre.blit(cartes[shuffled[y][x]], (x * 80 + 30 , y * 118 + 30))
##        print(shuffled)

        ## affiche contour carte depart
        if select_depart:
            #pygame.draw.rect(fenetre, (0, 0, 255), ((coord_depart[0] * 80 + 30 , coord_depart[1] * 118 + 30), (75 , 113)), 3)
            fenetre.blit(select1, (coord_depart[0] * 80 + 30 , coord_depart[1] * 118 + 30)) ############TEST select transparence

        ## affiche contour emplacement dest
        if select_dest:
            #pygame.draw.rect(fenetre, (255, 255, 0), ((coord_dest[0] * 80 + 30 , coord_dest[1] * 118 + 30), (75 , 113)), 3)
            fenetre.blit(select2, (coord_dest[0] * 80 + 30 , coord_dest[1] * 118 + 30)) #########TEST select transparence

        pygame.display.flip()

        if select_dest:
            if check_move(shuffled, coord_depart, coord_dest, regles):
                shuffled[coord_dest[1]][coord_dest[0]] = shuffled[coord_depart[1]][coord_depart[0]]
                shuffled[coord_depart[1]][coord_depart[0]] = "V00"
                game_started = True ## le jeu a commence
##            shuffled = check_move_new(shuffled, coord_depart, coord_dest, regles)
            select_depart,select_dest = False, False
            time.sleep(0.2) ## pour qu'il y ait une ptite pause pour qu'on voit bien les couleurs des contours


        if check_end(shuffled, lignes, colonnes, regles):
            end_game("win")

        
        ##resest variables
        tableauX, tableauY = (-1,-1)
        

def check_move(shuffled, move_from, move_to, regles):

    ordre = ordre_valeurs(regles, "start")

    valid = False
    
    type_carte_depart = shuffled[move_from[1]][move_from[0]][0]
    num_carte_depart = int(shuffled[move_from[1]][move_from[0]][1:3])

    ## les variables compare correspondent à la carte juste avant l'emplacement d'arrivee dans une meme ligne
    type_carte_compare = shuffled[move_to[1]][move_to[0] - 1][0]
    num_carte_compare = int(shuffled[move_to[1]][move_to[0] - 1][1:3])
    
    try:
        compare = ordre.index(num_carte_depart) - ordre.index(num_carte_compare)
    except ValueError:
        compare = -1

    if move_to[0] > 0 and shuffled[move_to[1]][move_to[0]] == "V00":
        if type_carte_depart == type_carte_compare and compare == 1:
            valid = True
    elif move_to[0] == 0 and num_carte_depart == 1 and shuffled[move_to[1]][move_to[0]] == "V00":
        valid = True
    ## si regles == 7, il n'y a pas d'as, donc le jeu commence avec le 7
    elif regles == 7 and move_to[0] == 0 and num_carte_depart == 7 and shuffled[move_to[1]][move_to[0]] == "V00":
        valid = True

    return(valid)


def check_end(shuffled, lignes, colonnes, regles): #### A VERIFIER

    temp = 0
    break_loop = False
    num1 = 0
    num2 = 0
    type1 = ""
    type2 = ""

    ordre = ordre_valeurs(regles, "start")
        
    for y in range(lignes):
        for x in range(colonnes - 1): # -1 pour pouvoir comparer un a un
##            les try except permettent d'eliminer l'erreur ou il regarde les cases vides (parce que num_casesvides = 0 et 0 pas dans ordre)
            try:
                num1 = ordre.index(int(shuffled[y][x][1:]))
            except ValueError:
                num1 = -1
            try:
                num2 = ordre.index(int(shuffled[y][x+1][1:]))
            except ValueError:
                num2 = -1
            type1 = shuffled[y][x][0]
            type2 = shuffled[y][x+1][0]
            if not (type1 == type2 and (num1 + 1) == num2):
                return(False)

    return(True)


def end_game(outcome):
    print(outcome)

def main():
    napoleon('simpsons',52)


# ==============================================================================
if __name__ == '__main__':
  main()
