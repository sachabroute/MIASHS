import pygame
from pygame.locals import *
import sys
import napoleon
import golf
import solitaire
from fonctions_generales import *

pygame.init()
pygame.display.set_caption("MIASHS")

fenetre = pygame.display.set_mode((1200, 675))

dico_images = images("images/menus/")
print(dico_images)

fond = pygame.image.load("images/fond/fond.png").convert()


while True:
    for event in pygame.event.get():
        mouseX, mouseY = pygame.mouse.get_pos()

        fenetre.blit(dico_images["fond.png"], (0,0))
        fenetre.blit(dico_images["klondike_off.png"], (50,105))
        fenetre.blit(dico_images["napoleon_off.png"], (550,105))
        fenetre.blit(dico_images["golf_off.png"], (50,370))
        fenetre.blit(dico_images["coin_off.png"], (550,390))
        
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_1:
                print("1")
                napoleon.main()
            elif event.key == K_2:
                print("2")
                golf.main()
            elif event.key == K_3:
                print("3")
                solitaire.main()

        elif event.type == MOUSEBUTTONDOWN:
            
            if 100 < mouseX < 500+(150*(1-((mouseY-130)/225))) and 130 < mouseY < 355 :
                print("klondike")
                solitaire.main()
            elif 500+(200*(1-((mouseY-130)/225))) < mouseX < 1100 and 130 < mouseY < 355 :
                print("napoleon")
                napoleon.main()
            elif 100 < mouseX < 500+(150*(1-((mouseY-405)/225))) and 405 < mouseY < 630 :
                print("golf")
                golf.main()

        elif event.type == MOUSEMOTION :
            if 100 < mouseX < 500+(150*(1-((mouseY-130)/225))) and 130 < mouseY < 355 :
                fenetre.blit(dico_images["klondike_on.png"], (50,105))
            elif 500+(200*(1-((mouseY-130)/225))) < mouseX < 1100 and 130 < mouseY < 355 :
                fenetre.blit(dico_images["napoleon_on.png"], (550,105))
            elif 100 < mouseX < 500+(150*(1-((mouseY-405)/225))) and 405 < mouseY < 630 :
                fenetre.blit(dico_images["golf_on.png"], (50,370))
            elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 405 < mouseY < 466 :
                fenetre.blit(dico_images["coin_on1.png"], (550,390))
            elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 487 < mouseY < 548 :
                fenetre.blit(dico_images["coin_on2.png"], (550,390))
            elif 500+(200*(1-((mouseY-405)/225))) < mouseX < 1100 and 569 < mouseY < 630 :
                fenetre.blit(dico_images["coin_on3.png"], (550,390))

    pygame.display.flip()
