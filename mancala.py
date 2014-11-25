import pygame
from pygame.locals import *
import sys


pygame.init()

fenetre = pygame.display.set_mode((800,500))

def main():

##    restart = 'o'
##    plateau_jeu = [4 for i in range(14)]
##    plateau_jeu[0], plateau_jeu[13]= 0, 0
##
##    while restart == 'o':
##
##        for i in range(2):
##            print(plateau_jeu[7*i:7*i+7])
##
##        pos = int(input("Entrer position: "))
##
##        for i in range(1, plateau_jeu[pos]+1):
##            print(i)
##            plateau_jeu[pos + i] += 1
##        plateau_jeu[pos] = 0
##
##        for i in range(2):
##            print(plateau_jeu[7*i:7*i+7])
##
##        restart = input("restart? o/n: ")

    nbre_cases = 6

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()


        pygame.draw.rect(fenetre, (155,155,155), (50,50,700,300),0)

        pygame.draw.rect(fenetre, (200,200,200), (75,100,75,200),0)
        pygame.draw.rect(fenetre, (200,200,200), (650,100,75,200),0)

        for x in range(nbre_cases):
            for y in range(2):
                pygame.draw.rect(fenetre, (150,150,210), (x*80+170,y*100+110,60,80),0)

        pygame.display.flip()


        



# ------------------------------------------------------------------------------
if __name__ == "__main__":
  main()
# ==============================================================================
