import pygame
from pygame.locals import *
import sys
import os
import time
from random import *

def main():
    options((1020, 720))

def options(taille_fenetre):
    pygame.init()
    pygame.display.set_caption("MIASHS")

    fenetre = pygame.display.set_mode(taille_fenetre)

    fond = pygame.image.load("images/fond/fond.png")


    nombre_cartes = 7 #### 7 pour que ca montre pas toutes les cartes sinon c'est chiant
    type_cartes = 'simpsons'
    liste_images_brutes = os.listdir("images/" + type_cartes + "/cartes/") ##Insère toutes les images du répertoire dans une liste    

    liste_images = []
    for i in range(nombre_cartes):
        liste_images.append(liste_images_brutes[i][:3])


    jeux_cartes = ['simpsons', 'pokemon', 'classic']

    dico = {}

    for type_carte in jeux_cartes:
        dico[type_carte + "4"] = pygame.image.load("images/" + type_carte + "/cartes/D11.png").convert_alpha()
        dico[type_carte + "5"] = pygame.image.load("images/" + type_carte + "/cartes/D12.png").convert_alpha()
        dico[type_carte + "6"] = pygame.image.load("images/" + type_carte + "/cartes/D13.png").convert_alpha()
        dico[type_carte + "fond"] = pygame.image.load("images/" + type_carte + "/dos/dos.png").convert_alpha()

    myfont = pygame.font.SysFont("monospace", 30)
    myfont2 = pygame.font.SysFont("monospace", 20)
    type_jeu = 'simpsons'
    taille_jeu = 28


    while True:        
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                ## pour le type de jeu
                if 20 <= mouseX <= 20 + 560 and 35 <= mouseY <= 35 + 140:
                    type_jeu = 'simpsons'
                elif 20 <= mouseX <= 20 + 560 and 35 + 140 <= mouseY <= 35 + (140*2):
                    type_jeu = 'pokemon'
                elif 20 <= mouseX <= 20 + 560 and 35 + (140*2) <= mouseY <= 35 + (140*3):
                    type_jeu = 'classic'
                ## pour la taille du jeu
                elif 160 <= mouseX <= 180 and 540 <= mouseY <= 580:
                    taille_jeu = 28
                elif 460 <= mouseX <= 480 and 540 <= mouseY <= 580:
                    taille_jeu = 32
                elif 160 <= mouseX <= 180 and 580 <= mouseY <= 600:
                    taille_jeu = 52
                elif 460 <= mouseX <= 480 and 580 <= mouseY <= 600:
                    taille_jeu = 56
                elif 260 <= mouseX <= 280 and 620 <= mouseY <= 640:
                    taille_jeu = 64

            elif event.type == KEYDOWN:
                if event.key == K_o:
                    return
                

        fenetre.blit(fond, (0,0))
        
## Affiche les jeux de cartes
        count = 0
        for type_carte in jeux_cartes:
            ## Affiche un rectangle gris qui sera autour des differents paquets de cartes
            pygame.draw.rect(fenetre, (150,150,150), (20, 35 + (count*140), 560, 130), 0)
            ##Affiche le message a gauche des cartes
            label = myfont.render("Theme : ", 1, (255,255,0))
            fenetre.blit(label, (40, 65 + (count*140)))
            label = myfont.render(type_carte, 1, (255,255,0))
            fenetre.blit(label, (40, 105 + (count*140)))
            for i in range(nombre_cartes):
                if i > 3:
                    fenetre.blit(dico[type_carte + "%s" %(i)], (240 + (i*40), 44 + (count*140)))
                else:
                    fenetre.blit(dico[type_carte + "fond"], (240 + (i*40), 44 + (count*140)))
            count += 1


## Affiche contour du jeu selectionne
        position_jeu = jeux_cartes.index(type_jeu)
        pygame.draw.rect(fenetre, (50,250,50), (20, 35 + (position_jeu*140), 560, 130), 3)


## Affiche rectangle gris autours de l'option taille du jeu
        pygame.draw.rect(fenetre, (40,40,40), (20, 460, 560, 200), 0)
## Affiche le text
        label
        label = myfont.render("Reglage de la taille du jeu", 1, (255,255,0))
        fenetre.blit(label, (40, 470))
        
        label = myfont2.render("28 cartes: ", 1, (255,255,0))
        fenetre.blit(label, (40, 540))
        label = myfont2.render("32 cartes: ", 1, (255,255,0))
        fenetre.blit(label, (340, 540))
        label = myfont2.render("52 cartes: ", 1, (255,255,0))
        fenetre.blit(label, (40, 580))
        label = myfont2.render("56 cartes: ", 1, (255,255,0))
        fenetre.blit(label, (340, 580))
        label = myfont2.render("64 cartes: ", 1, (255,255,0))
        fenetre.blit(label, (140, 620))

## Affiche des boites
        pygame.draw.rect(fenetre, (240,240,240), (160, 540, 21, 21),2)
        pygame.draw.rect(fenetre, (240,240,240), (460, 540, 21, 21),2)
        pygame.draw.rect(fenetre, (240,240,240), (160, 580, 21, 21),2)
        pygame.draw.rect(fenetre, (240,240,240), (460, 580, 21, 21),2)
        pygame.draw.rect(fenetre, (240,240,240), (260, 620, 21, 21),2)

## Affiche les checkmarks
        if taille_jeu == 28:
            pygame.draw.line(fenetre, (240,240,240), (160, 540),(180, 560),2)
            pygame.draw.line(fenetre, (240,240,240), (160, 560),(180, 540),2)
        elif taille_jeu == 32:
            pygame.draw.line(fenetre, (240,240,240), (460, 540),(480, 560),2)
            pygame.draw.line(fenetre, (240,240,240), (460, 560),(480, 540),2)
        elif taille_jeu == 52:
            pygame.draw.line(fenetre, (240,240,240), (160, 580),(180, 600),2)
            pygame.draw.line(fenetre, (240,240,240), (160, 600),(180, 580),2)
        elif taille_jeu == 56:
            pygame.draw.line(fenetre, (240,240,240), (460, 580),(480,600),2)
            pygame.draw.line(fenetre, (240,240,240), (460, 600),(480,580),2)
        elif taille_jeu == 64:
            pygame.draw.line(fenetre, (240,240,240), (260, 620),(280, 640),2)
            pygame.draw.line(fenetre, (240,240,240), (260, 640),(280, 620),2)
            

        pygame.display.flip()


# ==============================================================================
if __name__ == '__main__':
  main()
