import pygame
from pygame import *
from pygame.locals import *
import time
import sys
import napoleon
import golf
import solitaire
from fonctions_generales import *
import options

def credit(fenetre) :

    creditsound = pygame.mixer.Sound("credits.wav")
    creditsound.play()
    
    dico_images = images("images/credits/")
    liste_images = list(dico_images)
    print(dico_images, liste_images)
    
    for i in range(len(dico_images)) :
        for j in range(255,0,-4) :
            fenetre.blit(dico_images[liste_images[i]], (0,0))
            fenetre.fill((j,j,j), special_flags=BLEND_RGB_SUB)
            pygame.time.delay(15)
            pygame.display.flip()
        pygame.time.delay(5000)
        for j in range(0,255,4) :
            fenetre.fill(0x040404, special_flags=BLEND_RGB_SUB)
            pygame.time.delay(15)
            pygame.display.flip()
        pygame.time.delay(2000)

    main()
    
def main() :
    pygame.init()
    pygame.display.set_caption("MIASHS")

    fenetre = pygame.display.set_mode((1200, 675))

    dico_images = images("images/menus/")

    fond = pygame.image.load("images/fond/fond.png").convert()

    ## valeurs par default
    type_cartes = 'simpsons'
    taille_jeu = 52
    nombre_paquets = 1

    all_options = True

    while True:
        for event in pygame.event.get():
            mouseX, mouseY = pygame.mouse.get_pos()

            fenetre.blit(dico_images["fond.png"], (0,0))
            fenetre.blit(dico_images["klondike_off.png"], (50,105))
            fenetre.blit(dico_images["napoleon_off.png"], (550,105))
            fenetre.blit(dico_images["golf_off.png"], (50,370))
            fenetre.blit(dico_images["coin_off.png"], (550,395))
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                
                if 100 < mouseX < 500+(150*(1-((mouseY-130)/225))) and 130 < mouseY < 355 :
                    print("klondike")
                    solitaire.solitaire(type_cartes, taille_jeu, nombre_paquets)
                elif 500+(200*(1-((mouseY-130)/225))) < mouseX < 1100 and 130 < mouseY < 355 :
                    print("napoleon")
                    napoleon.napoleon(type_cartes, taille_jeu)
                elif 100 < mouseX < 500+(150*(1-((mouseY-405)/225))) and 405 < mouseY < 630 :
                    print("golf")
                    golf.golf(type_cartes, taille_jeu)
                elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 405 < mouseY < 466 :
                    print("options")
                    type_cartes, taille_jeu, nombre_paquets = options.options(fenetre, type_cartes, taille_jeu, nombre_paquets, all_options)
                elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 487 < mouseY < 548 :
                    print("credits")
                    credit(fenetre)
                elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 569 < mouseY < 630 :
                    print("quitter")
                    pygame.quit()
                    sys.exit()

            elif event.type == MOUSEMOTION :
                if 100 < mouseX < 500+(150*(1-((mouseY-130)/225))) and 130 < mouseY < 355 :
                    fenetre.blit(dico_images["klondike_on.png"], (50,105))
                elif 500+(200*(1-((mouseY-130)/225))) < mouseX < 1100 and 130 < mouseY < 355 :
                    fenetre.blit(dico_images["napoleon_on.png"], (550,105))
                elif 100 < mouseX < 500+(150*(1-((mouseY-405)/225))) and 405 < mouseY < 630 :
                    fenetre.blit(dico_images["golf_on.png"], (50,370))
                elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 405 < mouseY < 466 :
                    fenetre.blit(dico_images["coin_on1.png"], (550,395))
                elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 487 < mouseY < 548 :
                    fenetre.blit(dico_images["coin_on2.png"], (550,395))
                elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 569 < mouseY < 630 :
                    fenetre.blit(dico_images["coin_on3.png"], (550,395))

        pygame.display.flip()

if __name__ == '__main__':
  main()   
