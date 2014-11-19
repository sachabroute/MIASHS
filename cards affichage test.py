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
    cartes = {}
    for i in range(nombre_cartes):
        indice = liste_images_regles[i].split(".")[0]
        cartes["%s" %(indice)] = pygame.image.load("images/simpsons/cartes/"+liste_images_regles[i]).convert_alpha()

    ##Creation d'une liste de base, et melange de cartes
    liste_cartes = [name for name in cartes]
    shuffle(liste_cartes)
    shuffled = [liste_cartes[x:x+colonnes] for x in range(0, len(liste_cartes), colonnes)]
    
    ##Rajout de cartes vides a la fin des listes
    cartes["V00"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
    for i in range(lignes):
        shuffled[i].append("V00")    

    mouse_coord = (-1,-1)
    mouse_X, mouse_Y = 0,0
    select_depart = False
    coord_depart = (-1,-1)
    select_dest = False
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
                if select_depart == False and 0 <= mouse_coord[0] < colonnes + 1 and 0 <= mouse_coord[1] < lignes:
                    coord_depart = mouse_coord
                    select_depart = True
                elif select_dest == False and 0 <= mouse_coord[0] < colonnes + 1 and 0 <= mouse_coord[1] < lignes:
                    coord_dest = mouse_coord
                    select_dest = True

        ## affiche fond
        fenetre.blit(fond, (0,0))
        
        ## affiche cartes
        for y in range(lignes):
            for x in range(colonnes + 1):
                fenetre.blit(cartes[shuffled[y][x]], (x * 80 + 30 , y * 118 + 30))

        ## affiche contour carte (+ 1 pour colonnes pour la colonne vide du depart)
        if select_depart == True:
            pygame.draw.rect(fenetre, (0, 0, 255), ((coord_depart[0] * 80 + 30 , coord_depart[1] * 118 + 30), (75 , 113)), 3)

        ## affiche contour carte (+ 1 pour colonnes pour la colonne vide du depart)
        if select_dest == True:
            pygame.draw.rect(fenetre, (255, 255, 0), ((coord_dest[0] * 80 + 30 , coord_dest[1] * 118 + 30), (75 , 113)), 3)
            check = True

        pygame.display.flip()

        if check == True:
            shuffled = check_move(shuffled, coord_depart, coord_dest, regles)
            select_depart,select_dest,check = False, False, False
            time.sleep(0.2)
        
        ##resest variables
        mouse_coord = (-1,-1)

        
def check_move(shuffled, move_from, move_to, regles):

    valid = False
    
    type_carte_depart = shuffled[move_from[1]][move_from[0]][0]
    num_carte_depart = int(shuffled[move_from[1]][move_from[0]][1:3])
    type_carte_compare = shuffled[move_to[1]][move_to[0] - 1][0]
    num_carte_compare = int(shuffled[move_to[1]][move_to[0] - 1][1:3])

    ordre_valeurs_cartes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 12, 13]
    ordre_selon_regles = []
    for i in range(len(ordre_valeurs_cartes)) :
        if ordre_valeurs_cartes[i] <= regles :
            ordre_selon_regles.append(ordre_valeurs_cartes[i])

    if move_to[0] > 0 and shuffled[move_to[1]][move_to[0]] == "V00":
        print(num_carte_depart, num_carte_compare, ordre_selon_regles.index(num_carte_depart), ordre_selon_regles.index(num_carte_compare))
        if (type_carte_depart == type_carte_compare) and (ordre_selon_regles.index(num_carte_depart) == ordre_selon_regles.index(num_carte_compare)+1) :
            valid = True

    elif move_to[0] == 0 and num_carte_depart == 1 and shuffled[move_to[1]][move_to[0]] == "V00":
        valid = True

    if valid == True:
        shuffled[move_to[1]][move_to[0]] = shuffled[move_from[1]][move_from[0]]
        shuffled[move_from[1]][move_from[0]] = "V00"
        return(shuffled)
    else:
        return(shuffled)


# ==============================================================================
if __name__ == '__main__':
  main()
