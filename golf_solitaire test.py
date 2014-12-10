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

    ##Chargement des images
    fond = pygame.image.load("images/fond/fond.png")

    options = pygame.image.load("images/rouage.png")

    ##Définition des règles
    regles = 13 ##Est égal à 13 ou 14
    fenetre = pygame.display.set_mode((60+(regles+1)*80, 750))
    
    ##Chargement des cartes
    liste_images_brutes = os.listdir("images/pokemon/cartes/") ##Insère toutes les images du répertoire dans une liste
    liste_images_regles = [] ##Nouvelle liste qui contiendra uniquement les images de jeu

    ##Boucle supprimant les cartes cavalier si égal à 13
    for i in range(len(liste_images_brutes)) :
        cardsplit = liste_images_brutes[i] #On prend du caractère [1] au caractère [2] pour avoir le numéro de carte.
        cardnumber = cardsplit[1:3]
        if int(cardnumber) <= regles : ##Si ce numéro est inférieur au nombre dans règles, alors on append, sinon rien.
            liste_images_regles.append(liste_images_brutes[i])

    ##Fin du chargement des images
    nombre_cartes = int(len(liste_images_regles)) ##Définit le nombre de cartes à partir de la taille de la liste

## a voir si on peut changer les lignes et colonnes par la suite
    lignes = 5
    colonnes = 7
    cartes = {} ## initialisation biblioteque vide
    
    for i in range(nombre_cartes):
        indice = liste_images_regles[i].split(".")[0] ## correspond au nom de chaque carte. on split pour enlever le '.png', on se retrouve avec 'C01', 'C02', etc...
        cartes["%s" %(indice)] = pygame.image.load("images/pokemon/cartes/"+liste_images_regles[i]).convert_alpha()
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
                click_type, ind = check_mouse(mouse_coord, tableau_cartes, len(pioche_cartes), colonnes)
                if click_type == "cartes" and carte_pioche != "V00":
                    coord_card = (mouse_coord[0] - 80) // 120, len(tableau_cartes[ind]) - 1
                    select_card = True

                elif click_type == "pioche":
                    try:
                        carte_pioche = pioche_cartes.pop()
                    except IndexError:
                        end_game('loss')

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

        ##ENDGAME
        if tableau_cartes == []:
            end_game('win')
        
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


def check_mouse(mouse, tableau_cartes, nbre_pioche, colonnes):

    for i in range(colonnes):
        if (i * 120) + 80 <= mouse[0] < (i * 120) + 80 + 75 and ((len(tableau_cartes[i]) - 1) * 50) + 30 <= mouse[1] < ((len(tableau_cartes[i]) - 1) * 50) + 30 + 118:
            return("cartes",i)

    if 80 <= mouse[0] < (nbre_pioche * 5) + 80 + 75 and 400 <= mouse[1] < 400 + 118:
        return("pioche",'')

    return('','')

def end_game(outcome):
    print(outcome)
    


# ==============================================================================
if __name__ == '__main__':
  main()
