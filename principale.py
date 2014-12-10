import pygame
from pygame.locals import *
import sys
import napoleon
import golf_solitaire as golf
import solitaire3 as solitaire

pygame.init()
pygame.display.set_caption("MIASHS")

fenetre = pygame.display.set_mode((1025, 720))

fond = pygame.image.load("images/fond/fond.png").convert()


while True:
    for event in pygame.event.get():
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
            mouseX, mouseY = pygame.mouse.get_pos()
            if 25 <= mouseX <= 25 + 475 and 25 <= mouseY <= 25 + 325:
                print("napoleon")
                napoleon.main()
            elif 25 + 475 + 25 <= mouseX <= 25 + 475 + 25 + 475 and 25 <= mouseY <= 25 + 325:
                print("golf")
                golf.main()
            elif 25 <= mouseX <= 25 + 475 and 25 + 325 + 25 <= mouseY <= 25 + 325 + 25 + 325:
                print("solitaire")
                napoleon.main()
                

    fenetre.blit(fond, (0,0))

    pygame.draw.rect(fenetre, (150,150,150), (25,25,475,325), 0)
    pygame.draw.rect(fenetre, (150,150,150), (525,25,475,325), 0)
    pygame.draw.rect(fenetre, (150,150,150), (25,375,475,325), 0)

    pygame.display.flip()
