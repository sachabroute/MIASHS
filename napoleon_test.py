import pygame
from pygame.locals import *
import sys
import os
import time
from random import *

def main():
    pygame.init()
    pygame.display.set_caption("MIASHS")

    ##Chargement des images
    fond = pygame.image.load("images/fond/fond.png")

    options = pygame.image.load("images/rouage.png")

    ##Définition des règles
    regles = 13 ##Est égal à 13 ou 14
    fenetre = pygame.display.set_mode((60+(regles+1)*80, 750))
    
    ##Chargement des cartes
    liste_images_brutes = os.listdir("images/simpsons/cartes/") ##Insère toutes les images du répertoire dans une liste
    liste_images_regles = [] ##Nouvelle liste qui contiendra uniquement les images de jeu

    ##Boucle supprimant les cartes cavalier si égal à 13
    for i in range(len(liste_images_brutes)) :
        cardsplit = liste_images_brutes[i] #On prend du caractère [1] au caractère [2] pour avoir le numéro de carte.
        cardnumber = cardsplit[1:3]
        if int(cardnumber) <= regles : ##Si ce numéro est inférieur au nombre dans règles, alors on append, sinon rien.
            liste_images_regles.append(liste_images_brutes[i])

    ##Fin du chargement des images
    nombre_cartes = int(len(liste_images_regles)) ##Définit le nombre de cartes à partir de la taille de la liste

    lignes = 4
    colonnes = int(nombre_cartes / lignes)
    cartes = {} ## initialisation biblioteque vide
    
    for i in range(nombre_cartes):
        indice = liste_images_regles[i].split(".")[0] ## correspond au nom de chaque carte. on split pour enlever le '.png', on se retrouve avec 'C01', 'C02', etc...
        cartes["%s" %(indice)] = pygame.image.load("images/simpsons/cartes/"+liste_images_regles[i]).convert_alpha()
    #### end load images (wouaaah c'est super court t'as vu!??)

    ## creation d'une liste de base, et melange de cartes
    liste_cartes = [name for name in cartes] ## prends chaque nom de cartes dans la biblioteque

    ## rajout de cartes vides a la fin des listes.
    cartes["V00"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
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

########## TEST options
    options = pygame.image.load("images/rouage.png").convert_alpha()
    F_long, F_larg = 60+(regles+1)*80, 750
##########
                

    mouse_coord = (-1,-1)
    mouse_X, mouse_Y = 0,0
    select_depart = False ## variable si la carte de depart a été selectionnée
    coord_depart = (-1,-1)
    select_dest = False ## variable si la carte de destination a été selectionnée
    coord_dest = (-1,-1)
    check = False

    while True:        
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                ## conversion coordonnées brutes en coordonnées tableau
                mouse_coord = (mouse_coord[0] - 30) // 80, (mouse_coord[1] - 30) // 118
                if select_depart == False and 0 <= mouse_coord[0] < colonnes + 1 and 0 <= mouse_coord[1] < lignes and shuffled[mouse_coord[1]][mouse_coord[0]] != "V00": ## pour la carte de depart
                    coord_depart = mouse_coord
                    select_depart = True
                ## si l'utilisateur click sur une carte au lieu du vide en deuxieme choix
                elif select_dest == False and 0 <= mouse_coord[0] < colonnes + 1 and 0 <= mouse_coord[1] < lignes and shuffled[mouse_coord[1]][mouse_coord[0]] != "V00":
                    coord_depart = mouse_coord
                    select_depart = True
                elif select_dest == False and 0 <= mouse_coord[0] < colonnes + 1 and 0 <= mouse_coord[1] < lignes and shuffled[mouse_coord[1]][mouse_coord[0]] == "V00": ## pour la position de destination
                    coord_dest = mouse_coord
                    select_dest = True
                elif F_long - 35 <= mouse_coord[0] <= F_long - 35 + 30 and 5 <= mouse_coord[1] <= 5 + 30:
                    options()


        ## affiche fond
        fenetre.blit(fond, (0,0))

################ AFFICHE test options
        fenetre.blit(options, (F_long - 35, 5))
        
        ## affiche cartes
        for y in range(lignes):
            for x in range(colonnes + 1): # + 1 pour rajouter la carte vide à la fin de chaque ligne
                fenetre.blit(cartes[shuffled[y][x]], (x * 80 + 30 , y * 118 + 30))

        ## affiche contour carte depart
        if select_depart:
            #pygame.draw.rect(fenetre, (0, 0, 255), ((coord_depart[0] * 80 + 30 , coord_depart[1] * 118 + 30), (75 , 113)), 3)
            fenetre.blit(select1, (coord_depart[0] * 80 + 30 , coord_depart[1] * 118 + 30)) ############TEST select transparence

        ## affiche contour emplacement dest
        if select_dest:
            #pygame.draw.rect(fenetre, (255, 255, 0), ((coord_dest[0] * 80 + 30 , coord_dest[1] * 118 + 30), (75 , 113)), 3)
            fenetre.blit(select2, (coord_dest[0] * 80 + 30 , coord_dest[1] * 118 + 30)) #########TEST select transparence
            check = True
            print(shuffled)

        pygame.display.flip()

        if select_dest:
            shuffled = check_move(shuffled, coord_depart, coord_dest, regles)
            select_depart,select_dest = False, False
            time.sleep(0.2) ## pour qu'il y ait une ptite pause pour qu'on voit bien les couleurs des contours

        if check_end(shuffled, lignes, colonnes):
            end_game()

        
        ##resest variables
        mouse_coord = (-1,-1)

        
def check_move(shuffled, move_from, move_to, regles):

    valid = False
    
    type_carte_depart = shuffled[move_from[1]][move_from[0]][0]
    num_carte_depart = int(shuffled[move_from[1]][move_from[0]][1:3])

    ## les variables compare correspondent à la carte juste avant l'emplacement d'arrivee dans une meme ligne
    type_carte_compare = shuffled[move_to[1]][move_to[0] - 1][0]
    num_carte_compare = int(shuffled[move_to[1]][move_to[0] - 1][1:3])


    ordre_valeurs_cartes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 12, 13]
    ordre_selon_regles = []
    for i in range(len(ordre_valeurs_cartes)) :
        if ordre_valeurs_cartes[i] <= regles :
            ordre_selon_regles.append(ordre_valeurs_cartes[i])

    if move_to[0] > 0 and shuffled[move_to[1]][move_to[0]] == "V00":
        if (type_carte_depart == type_carte_compare) and (ordre_selon_regles.index(num_carte_depart) == ordre_selon_regles.index(num_carte_compare)+1) :
            valid = True

    elif move_to[0] == 0 and num_carte_depart == 1 and shuffled[move_to[1]][move_to[0]] == "V00": ## si la carte est un as et est déplacé vers la première colonne
        valid = True

    if valid == True:
        shuffled[move_to[1]][move_to[0]] = shuffled[move_from[1]][move_from[0]]
        shuffled[move_from[1]][move_from[0]] = "V00"

    return(shuffled)


def check_end(shuffled, lignes, colonnes):

    temp = 0
    break_loop = False
    
    for y in range(lignes):
        for x in range(colonnes - 1): # -1 pour pouvoir comparer un a un
            temp = shuffled[y][x]
            if temp >= shuffled[y][x+1]:
                return(False)

    return(True)

def options():

    cartes_1 =
    cartes_2 =
    cartes_3 =
            


# ==============================================================================
if __name__ == '__main__':
  main()
