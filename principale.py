import pygame
from pygame.locals import *
import sys
import napoleon
import golf_solitaire as golf
import solitaire3 as solitaire

pygame.init()
pygame.display.set_caption("MIASHS")

fenetre = pygame.display.set_mode((1020, 720))


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
