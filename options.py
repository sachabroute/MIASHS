import pygame
from pygame.locals import *
import sys
import os
import time
from random import *


def main():
    pygame.init()
    fenetre = pygame.display.set_mode((1200,675))
    options(fenetre, 'simpsons', 52, 1, True)
    pygame.quit()
    sys.exit()

def options(fenetre, type_cartes, taille_jeu, nombre_paquets, all_options):

    fenetreX, fenetreY = fenetre.get_size()
    
    liste_images = os.listdir("images/menu_option/")

    dico_images = {}

    for element in liste_images:
        dico_images[element] = pygame.image.load("images/menu_option/"+element).convert_alpha()

    dico_images["blur.png"] = pygame.transform.scale(dico_images["blur.png"], (fenetreX, fenetreY))
    
    restart = False
    
    ## cache le jeu en cours, on le blit ici pour pas qu'il se blit plein de fois
    if not all_options:
        fenetre.blit(dico_images["blur.png"], (0,0))

    while True:

        mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if 50 <= mouseX <= 350 and 170 <= mouseY <= 390:
                    if type_cartes != "simpsons":
                        type_cartes = "simpsons"
                elif 350 <= mouseX <= 650 and 170 <= mouseY <= 390:
                    if type_cartes != "pokemon":
                        type_cartes = "pokemon"
                elif 50 <= mouseX <= 350 and 420 <= mouseY <= 740:
                    if type_cartes != "classic":
                        type_cartes = "classic"
                ## pour le bouton restart
                elif not all_options and 650 <= mouseX <= 775 and 550 <= mouseY <= 675:
                    if restart:
                        restart = False
                    else:
                        restart = True
                ## pour la fleche retour au jeu
                elif 730 <= mouseX <= 760 and 40 <= mouseY <= 70:
                    if all_options:
                        return(type_cartes, taille_jeu, nombre_paquets)
                    else:
                        return(type_cartes, restart)

                ## si all_options, pour la taille du jeu
                elif all_options and 800 <= mouseX <= 900 and 180 <= mouseY <= 330:
                    taille_jeu = 28
                elif all_options and 1000 <= mouseX <= 1100 and 180 <= mouseY <= 330:
                    taille_jeu = 32
                elif all_options and 900 <= mouseX <= 1000 and 335 <= mouseY <= 485:
                    taille_jeu = 52
                elif all_options and 800 <= mouseX <= 900 and 490 <= mouseY <= 640:
                    taille_jeu = 56
                elif all_options and 1000 <= mouseX <= 1100 and 490 <= mouseY <= 640:
                    taille_jeu = 64

                ## pour le nombre de paquets
                elif 430 <= mouseX <= 480 and 510 <= mouseY <= 560:
                    nombre_paquets = 1
                elif 540 <= mouseX <= 590 and 510 <= mouseY <= 560:
                    nombre_paquets = 2
                elif 430 <= mouseX <= 480 and 575 <= mouseY <= 625:
                    nombre_paquets = 3
                elif 540 <= mouseX <= 590 and 575 <= mouseY <= 625:
                    nombre_paquets = 4

        ## affiche fond
        if all_options:
            fenetre.blit(dico_images["full_fond.png"], (0,0))


        ## affiche le text
        if all_options:
            fenetre.blit(dico_images["full_text.png"], (0,0))
        else:
            fenetre.blit(dico_images["text.png"], (0,0))

        ## Affiche le fleche de retour
        fenetre.blit(dico_images["retour.png"], (730, 40))
        ## Affiche si la souris est au dessus de la fleche retour
        if 730 <= mouseX <= 760 and 40 <= mouseY <= 70:
            fenetre.blit(dico_images["retour_select.png"], (730, 40))

        ## affiche les simpsons
        if type_cartes == "simpsons":
            fenetre.blit(dico_images["options_simpsons_color.png"], (50, 170))
        else:
            fenetre.blit(dico_images["options_simpsons_gray.png"], (50, 170))
        if 50 <= mouseX <= 350 and 170 <= mouseY <= 390:
            fenetre.blit(dico_images["options_simpsons_color.png"], (50, 170))            

        ## affiche les pokemons
        if type_cartes == "pokemon":
            fenetre.blit(dico_images["options_pokemon_color.png"], (350, 170))
        else:
            fenetre.blit(dico_images["options_pokemon_gray.png"], (350, 170))
        if 350 <= mouseX <= 650 and 170 <= mouseY <= 390:
            fenetre.blit(dico_images["options_pokemon_color.png"], (350, 170))

        ## affiche les classic
        if type_cartes == "classic":
            fenetre.blit(dico_images["options_classic_color.png"], (50, 420))
        else:
            fenetre.blit(dico_images["options_classic_gray.png"], (50, 420))
        if 50 <= mouseX <= 350 and 420 <= mouseY <= 740:
            fenetre.blit(dico_images["options_classic_color.png"], (50, 420))

    ## si all_options, affiche les paquets de cartes
        if all_options:
            ## affiche 28 cartes
            if taille_jeu == 28:
                fenetre.blit(dico_images["28_color.png"],(800, 180))
                fenetre.blit(dico_images["32_gray.png"],(1000, 180))
                fenetre.blit(dico_images["52_gray.png"],(900, 335))
                fenetre.blit(dico_images["56_gray.png"],(800, 490))
                fenetre.blit(dico_images["64_gray.png"],(1000, 490))
            ## affiche 32 cartes
            elif taille_jeu == 32:
                fenetre.blit(dico_images["28_gray.png"],(800, 180))
                fenetre.blit(dico_images["32_color.png"],(1000, 180))
                fenetre.blit(dico_images["52_gray.png"],(900, 335))
                fenetre.blit(dico_images["56_gray.png"],(800, 490))
                fenetre.blit(dico_images["64_gray.png"],(1000, 490))
            ## affiche 52 cartes
            elif taille_jeu == 52:
                fenetre.blit(dico_images["28_gray.png"],(800, 180))
                fenetre.blit(dico_images["32_gray.png"],(1000, 180))
                fenetre.blit(dico_images["52_color.png"],(900, 335))
                fenetre.blit(dico_images["56_gray.png"],(800, 490))
                fenetre.blit(dico_images["64_gray.png"],(1000, 490))
            ## affiche 56 cartes
            elif taille_jeu == 56:
                fenetre.blit(dico_images["28_gray.png"],(800, 180))
                fenetre.blit(dico_images["32_gray.png"],(1000, 180))
                fenetre.blit(dico_images["52_gray.png"],(900, 335))
                fenetre.blit(dico_images["56_color.png"],(800, 490))
                fenetre.blit(dico_images["64_gray.png"],(1000, 490))
            ## affiche 64 cartes
            elif taille_jeu == 64:
                fenetre.blit(dico_images["28_gray.png"],(800, 180))
                fenetre.blit(dico_images["32_gray.png"],(1000, 180))
                fenetre.blit(dico_images["52_gray.png"],(900, 335))
                fenetre.blit(dico_images["56_gray.png"],(800, 490))
                fenetre.blit(dico_images["64_color.png"],(1000, 490))
            ##affiche si la souris est dessus
            if 800 <= mouseX <= 900 and 180 <= mouseY <= 330:
                fenetre.blit(dico_images["28_color.png"],(800, 180))
            elif 1000 <= mouseX <= 1100 and 180 <= mouseY <= 330:
                fenetre.blit(dico_images["32_color.png"],(1000, 180))
            elif 900 <= mouseX <= 1000 and 335 <= mouseY <= 485:
                fenetre.blit(dico_images["52_color.png"],(900, 335))
            elif 800 <= mouseX <= 900 and 490 <= mouseY <= 640:
                fenetre.blit(dico_images["56_color.png"],(800, 490))
            elif 1000 <= mouseX <= 1100 and 490 <= mouseY <= 640:
                fenetre.blit(dico_images["64_color.png"],(1000, 490))

            ## pour le nombre de paquets
            elif 430 <= mouseX <= 480 and 510 <= mouseY <= 560:
                pygame.draw.rect(fenetre, (150,150,150), (430, 510, 50, 50), 3)
            elif 540 <= mouseX <= 590 and 510 <= mouseY <= 560:
                pygame.draw.rect(fenetre, (150,150,150), (540, 510, 50, 50), 3)
            elif 430 <= mouseX <= 480 and 575 <= mouseY <= 625:
                pygame.draw.rect(fenetre, (150,150,150), (430, 575, 50, 50), 3)
            elif 540 <= mouseX <= 590 and 575 <= mouseY <= 625:
                pygame.draw.rect(fenetre, (150,150,150), (540, 575, 50, 50), 3)


            ## affiche nombre paquets
            if nombre_paquets == 1:
                pygame.draw.rect(fenetre, (255,255,255), (430, 510, 50, 50), 3)
            elif nombre_paquets == 2:
                pygame.draw.rect(fenetre, (255,255,255), (540, 510, 50, 50), 3)
            elif nombre_paquets == 3:
                pygame.draw.rect(fenetre, (255,255,255), (430, 575, 50, 50), 3)
            elif nombre_paquets == 4:
                pygame.draw.rect(fenetre, (255,255,255), (540, 575, 50, 50), 3)


        ## affiche le bouton restart si all_options == False
        if not all_options:
            if not restart:
                fenetre.blit(dico_images["restart_off.png"], (650, 550))
            elif restart:
                fenetre.blit(dico_images["restart_on.png"], (650, 550))
            if not restart and 650 <= mouseX <= 775 and 550 <= mouseY <= 675:
                fenetre.blit(dico_images["restart_hover.png"], (650, 550))



            
            

        pygame.display.flip()

# ==============================================================================
if __name__ == '__main__':
  main()
