import pygame
from pygame.locals import *
import sys
import os
import time
from random import *


def main():
    pygame.init()
    fenetre = pygame.display.set_mode((835,750))
    options(fenetre, 'simpsons')
    pygame.quit()
    sys.exit()

def options(fenetre, type_cartes):

    fenetreX, fenetreY = fenetre.get_size()
    
    liste_images = os.listdir("images/test/")

    dico_images = {}

    for element in liste_images:
        dico_images[element] = pygame.image.load("images/test/"+element).convert_alpha()

    dico_images["blur.png"] = pygame.transform.scale(dico_images["blur.png"], (fenetreX, fenetreY))

    restart = False
    
    ## cache le jeu en cours, on le blit ici pour pas qu'il se blit plein de fois
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
                elif 200 <= mouseX <= 500 and 420 <= mouseY <= 740:
                    if type_cartes != "classic":
                        type_cartes = "classic"
                ## pour le bouton restart
                elif 650 <= mouseX <= 775 and 550 <= mouseY <= 675:
                    if restart:
                        restart = False
                    else:
                        restart = True
                ## pour la fleche retour au jeu
                elif 730 <= mouseX <= 760 and 40 <= mouseY <= 70:
                    return(type_cartes, restart)


        ## affiche le text
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
            fenetre.blit(dico_images["options_classic_color.png"], (200, 420))
        else:
            fenetre.blit(dico_images["options_classic_gray.png"], (200, 420))
        if 200 <= mouseX <= 500 and 420 <= mouseY <= 740:
            fenetre.blit(dico_images["options_classic_color.png"], (200, 420))


        ## affiche le bouton restart
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
