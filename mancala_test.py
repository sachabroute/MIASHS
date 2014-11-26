import pygame
from pygame.locals import *
import sys


pygame.init()

fenetre = pygame.display.set_mode((800,500))

def main():

##    restart = 'o'

    nbre_cases = 6
    
    plateau_jeu = [[4 for x in range(nbre_cases + 1)] for y in range(2)]
    plateau_jeu[0][-1], plateau_jeu[1][-1]= 0, 0

    plateau_pygame = [[],[]]
    for y in range(2):
        for x in range(nbre_cases):
                plateau_pygame[y].append(pygame.Rect(x*80+170,y*100+110,60,80))
        if y == 0:  
            plateau_pygame[y].append(pygame.Rect(650,100,75,200))
        elif y == 1:
            plateau_pygame[y].append(pygame.Rect(75,100,75,200))
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

    while True:

        coords = (-1,-1)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                coords = check_mouse(nbre_cases, plateau_pygame, pygame.mouse.get_pos())
                print(coords)

        if coords != (-1,-1):
            tableau_jeu = move(tableau_jeu, coords)
                            
                
        
        myfont = pygame.font.SysFont("monospace", 15)


        pygame.draw.rect(fenetre, (155,155,155), (50,50,700,300),0)
        
        for y in range(2):
            for x in range(nbre_cases+1):
                pygame.draw.rect(fenetre, (200,200,250), plateau_pygame[y][x],0)

        label = myfont.render("%d" %(plateau_jeu[0][-1]), 1, (0,0,0))
        fenetre.blit(label, (75,100))
        
        label = myfont.render("%d" %(plateau_jeu[1][-1]), 1, (0,0,0))
        fenetre.blit(label, (650,100))


        for y in range(2):
            for x in range(nbre_cases):
                    label = myfont.render("%d" %(plateau_jeu[y][x]), 1, (0,0,0))
                    fenetre.blit(label, (x*80+170,y*100+110))


        pygame.display.flip()



def check_mouse(nbre_cases, plateau, mouse):
    
    for y in range(2):
        for x in range(nbre_cases):
            if x != nbre_cases and plateau[y][x].collidepoint(mouse):
                coords = ((mouse[0]- 170) // 80), ((mouse[1] - 110) // 100)
                if coords[1] == 0:
                    coords = nbre_cases-1-coords[0], 1
                else:
                    coords = coords[0], 0
                return(coords)
    return(-1,-1)


def move(tableau, x, y)

    for i in range(tableau[y][x]):
        tableau


# ------------------------------------------------------------------------------
if __name__ == "__main__":
  main()
# ==============================================================================
