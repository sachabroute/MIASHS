import pygame
from pygame.locals import *
import sys
import os
from random import *

pygame.init()
pygame.display.set_caption("MIASHS")
fenetre = pygame.display.set_mode((1175, 750))



#### load images
os.chdir("images/jeux_cartes/simpsons")
liste_images_brutes = os.listdir()
nombre_cartes = int(len(liste_images_brutes))
lignes = 4
colonnes = int(nombre_cartes / lignes)
liste_images = [[0 for i in range(2)] for i in range(nombre_cartes)]
for i in range(nombre_cartes):
    liste_images[i][0] = liste_images_brutes[i]
    liste_images[i][1] = pygame.image.load(liste_images_brutes[i]).convert_alpha()
os.chdir("../../fond")
fond = pygame.image.load("fond.png")
#### end load images (wouaaah c'est super court t'as vu!??)

## melange de cartes
shuffle(liste_images)
print(liste_images)

mouse_coord = (-1,-1)
mouse_X, mouse_Y = 0,0
select_depart = False
coord_depart = (-1,-1)
select_dest = False
coord_dest = (-1,-1)


while True:

    ##resest variables
    mouse_coord = (-1,-1)
    
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
        for x in range(colonnes):
                fenetre.blit(liste_images[y * 13 + x][1], (x * 80 + 30 , y * 118 + 30))

    ## affiche contour carte (+ 1 pour colonnes pour la colonne vide du depart)
    if select_depart == True:
        pygame.draw.rect(fenetre, (255, 0, 0), ((coord_depart[0] * 80 + 30 , coord_depart[1] * 118 + 30), (75 , 113)), 3)

    ## affiche contour carte (+ 1 pour colonnes pour la colonne vide du depart)
    if select_dest == True:
        pygame.draw.rect(fenetre, (0, 255, 0), ((coord_dest[0] * 80 + 30 , coord_dest[1] * 118 + 30), (75 , 113)), 3)

    pygame.display.flip()

        
def check_move(shuffled, move_from, move_to):

    valid = False
    
    carte = shuffled[move_from[1]][move_from[0]]
    carte = carte.split()
    carte[1] = int(carte[1])

    if move_to[0] > 0 and shuffled[move_to[1]][move_to[0]] == "":
        compare = shuffled[move_to[1]][move_to[0]].split()
        compare[1] = int(compare[1])

        if (carte[0] == compare[0]) and (carte[1] == compare[1] + 1):
            valid = True

    if move_to[0] == 0 and carte[0] == "1" and shuffled[move_to[1]][move_to[0]]:
        valid = True

    if valid == True:
        shuffled[move_to[1]][move_to[0]] = " ".join(carte)
        shuffled[move_from[1]][move_from[0]] = ""
        return(shuffled)
    else:
        return(shuffled)
