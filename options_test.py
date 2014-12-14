import pygame
from pygame.locals import *
import sys
import os
import time
from random import *

def main():
    pygame.init()
    fenetre = pygame.display.set_mode((835,750))

    pokemon_color = pygame.image.load("images/test/options_pokemon_color.png")
    pokemon_gray = pygame.image.load("images/test/options_pokemon_gray.png")

    select = False

    while True:

        mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    if select:
                        select = False
                    else:
                        select = True

        if not select:
            fenetre.blit(pokemon_gray, (100,100))
        else:
            fenetre.blit(pokemon_color, (100,100))
                
            
            

        pygame.display.flip()

# ==============================================================================
if __name__ == '__main__':
  main()
