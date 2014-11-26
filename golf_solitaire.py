import pygame
from pygame.locals import *
import sys
import os
import time
from random import *


def main():
    pygame.init()
    pygame.display.set_caption("MIASHS")
    fenetre = pygame.display.set_mode((1175, 750))



    #### load images
    fond = pygame.image.load("images/fond/fond.png")
    liste_images_brutes = os.listdir("images/pokemon/cartes/")
    nombre_cartes = int(len(liste_images_brutes))
    lignes = 5   ## a voir si on peut changer ces valeurs pour ce jeu
    colonnes = 7 ## a voir si on peut changer ces valeurs pour ce jeu
    cartes = {}
    for i in range(nombre_cartes):
        indice = liste_images_brutes[i].split(".")[0]
        cartes["%s" %(indice)] = pygame.image.load("images/pokemon/cartes/"+liste_images_brutes[i]).convert_alpha()
    #### end load images (wouaaah c'est super court t'as vu!??)

    ## creation d'une liste de base, et melange de cartes
    liste_cartes = [name for name in cartes]
    shuffle(liste_cartes)
    tableau_cartes = [liste_cartes[x:x+lignes] for x in range(0, colonnes * lignes, lignes)]
    pioche_cartes = liste_cartes[colonnes * lignes:]
    poubelle_cartes = []

    ## le dos des cartes (pour la pioche), carte vide
    dos = pygame.image.load("images/pokemon/dos/dos.png").convert_alpha()
    cartes["V00"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
    carte_pioche = "V00"
    

    mouse_coord = (-1,-1)
    select_card = False
    coord_card = (-1,-1)
    pioche = False


    while True:        
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_coord = pygame.mouse.get_pos()
                if check_mouse(mouse_coord, len(tableau_cartes), len(pioche_cartes), colonnes) == "cartes":
                    coord_card = (mouse_coord[0] - 80) // 120, len(tableau_cartes[i]) - 1
                    select_card = True

                if check_mouse(mouse_coord, len(tableau_cartes), len(pioche_cartes), colonnes) == "pioche":
                    carte_pioche = pioche_cartes.pop()

        ## affiche fond
        fenetre.blit(fond, (0,0))
        
        ## affiche cartes
        for x in range(colonnes):
            for y in range(lignes):
                try:
                    fenetre.blit(cartes[tableau_cartes[x][y]], (x * 120 + 80, y * 50 + 30))
                except:
                    break

        ## affiche pioche
        for i in range(len(pioche_cartes)):
            fenetre.blit(dos, (80 + i * 5, 400))

        ## affiche contour carte (+ 1 pour colonnes pour la colonne vide du depart)
        if select_card == True:
            pygame.draw.rect(fenetre, (0, 255, 0), ((coord_card[0] * 120 + 80 , coord_card[1] * 50 + 30), (75 , 113)), 3)


        fenetre.blit(cartes[carte_pioche], (300, 400))

        pygame.display.flip()

        if select_card:
            tableau_cartes, carte_pioche = check_move(tableau_cartes, carte_pioche, coord_card)
            select_card = False
            time.sleep(0.3)
        
        ##reset variables
        mouse_coord = (-1,-1)

    

        
def check_move(tableau_cartes, carte_pioche, coord_card):
    valid = False
    num_carte = int(tableau_cartes[coord_card[0]][coord_card[1]][1:3])
    num_carte_pioche = int(carte_pioche[1:3])

    if num_carte == num_carte_pioche + 1 or num_carte == num_carte_pioche - 1:
        carte_pioche = tableau_cartes[coord_card[0]][coord_card[1]]
        del(tableau_cartes[coord_card[0]][coord_card[1]])
    elif (num_carte == 13 and num_carte_pioche == 1) or (num_carte == 1 and num_carte_pioche == 13):
        carte_pioche = tableau_cartes[coord_card[0]][coord_card[1]]
        del(tableau_cartes[coord_card[0]][coord_card[1]])
    
    return(tableau_cartes, carte_pioche)


def check_mouse(mouse, nbre_cartes, nbre_pioche, colonnes):

    for i in range(colonnes):
        if i * 120 + 80 <= mouse[0] < i * 120 + 80 + 75 and (nbre_cartes - 1) * 50 + 30 <= mouse[1] < (nbre_cartes - 1) * 50 + 30 + 118:
            return("cartes")

    if 80 <= mouse[0] < (nbre_pioche * 5) + 80 + 75 and 400 <= mouse[1] < 400 + 118:
        return("pioche")
    


# ==============================================================================
if __name__ == '__main__':
  main()
