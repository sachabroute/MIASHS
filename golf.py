import pygame
from pygame.locals import *
import sys
import os
import time
from random import *
import options
import fonctions_generales
import principale


def images(cartes_alea, type_cartes):

    cartes = {}

    for i in range(len(cartes_alea)):
        try:
            cartes[cartes_alea[i]] = pygame.image.load("images/" + type_cartes + "/cartes/"+cartes_alea[i]).convert_alpha()
        except:
            pass
    return(cartes)



def golf(type_cartes, taille_jeu):
    pygame.init()
    pygame.display.set_caption("MIASHS")

    ##Définition des règles
    regles = int(taille_jeu / 4)
    ## determine les lignes et colonnes grace a regles
    lignes, colonnes = taille_golf(regles)
    
    fenetreX, fenetreY = 80+(colonnes*75)+((colonnes-1)*45)+80, 750
    fenetre = pygame.display.set_mode((fenetreX, fenetreY))

    ##Chargement des images
    fond = pygame.image.load("images/fond/fond.png").convert()
    fond = pygame.transform.scale(fond, (fenetreX, fenetreY))
    select = pygame.image.load("images/select.png").convert_alpha()
    repertoire_cartes = ("images/" + type_cartes + "/cartes/")
    liste_images = fonctions_generales.generation_jeu_aleatoire(repertoire_cartes, regles, 1) 
    cartes_dico = images(liste_images, type_cartes)

    ## creation d'une liste de base, et melange de cartes_dico
    liste_cartes = [name for name in cartes_dico]
    shuffle(liste_cartes)
    tableau_cartes = [liste_cartes[x:x+lignes] for x in range(0, colonnes * lignes, lignes)]
    pioche_cartes = liste_cartes[colonnes * lignes:]

    ## le dos des cartes_dico (pour la pioche), carte vide
    dos = pygame.image.load("images/" + type_cartes + "/dos/dos.png").convert_alpha()
    cartes_dico = rajoute_carte_vide(cartes_dico)
    carte_pioche = "V00.png"
    

    mouseX, mouseY = (-1,-1)
    select_card = False
    coord_card = (-1,-1)
    pioche = False
    myfont = pygame.font.SysFont("monospace", 20)
    allow_redo = False ## permet de limiter le nombre de 'redo's de l'utilisateur a une fois
    redo = False ## si l'utilisateur veux revenir en arriere d'un mouvement
    last_move = '' ## prends les valeurs 'pioche' ou 'tableau' pour indiquer le dernier type de mouvement de l'utilisateur
    regles_jeu = [regles, "start", "both+", "any", "hello", "golf"] ## a etre utilise pour la fonction check_move
    all_options = False

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
       
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                click_type, ind = check_mouse((mouseX, mouseY), tableau_cartes, len(pioche_cartes), colonnes, (fenetreX, fenetreY))
                if click_type == "cartes" and carte_pioche != "V00.png":
                    coord_card = (mouseX - 80) // 120, len(tableau_cartes[ind]) - 1
                    select_card = True
                    game_started = True
                    last_move = click_type
                elif click_type == "pioche":
                    memory_pioche = carte_pioche
                    carte_pioche = pioche_cartes.pop()
                    allow_redo = True
                    last_move = click_type
                elif selection == "menu":
                    principale.main()
                elif selection == "options":
                    type_cartes, restart = options.options(fenetre, type_cartes, taille_jeu, 1, all_options)
                    if restart:
                        golf(type_cartes, taille_jeu)
                    repertoire_cartes = "images/" + type_cartes + "/cartes/"
                    cartes_dico = images(liste_images, type_cartes)
                    cartes_dico = rajoute_carte_vide(cartes_dico)
                elif selection == "retour" and allow_redo:
                    start_time = pygame.time.get_ticks()
                    redo = True
                    

            elif event.type == KEYDOWN:
                if event.key == K_p:
                    print(fonctions_generales.ordre_valeurs(regles, "start"))

        ## affiche fond
        fenetre.blit(fond, (0,0))

        ## reviens en arriere d'un mouvement
        if redo:
            if last_move == 'cartes':
                tableau_cartes[memory_coord[0]].append(carte_pioche)
                carte_pioche = memory_pioche
                redo = False
                allow_redo = False
            elif last_move == 'pioche':
                pioche_cartes.append(carte_pioche)
                carte_pioche = memory_pioche
                redo = False
                allow_redo = False

        
        ## affiche cartes_dico
        for x in range(colonnes):
            for y in range(lignes):
                try:
                    fenetre.blit(cartes_dico[tableau_cartes[x][y]], (x * 120 + 80, y * 50 + 30))
                except:
                    break

        ## affiche pioche
        for i in range(len(pioche_cartes)):
            fenetre.blit(dos, (80 + i * 5, 400))
                

        ## affiche contour carte (+ 1 pour colonnes pour la colonne vide du depart)
        if select_card == True:
            fenetre.blit(select, (coord_card[0] * 120 + 80 , coord_card[1] * 50 + 30))

        ## affiche la carte visible
        fenetre.blit(cartes_dico[carte_pioche], (300, 400))

        ## affiche les boutons a droite
        selection = fonctions_generales.barre_laterale(fenetre, fenetreX, (mouseX,mouseY))


        pygame.display.flip()
            

        ## apres le display flip pour que le time.sleep soit precevable
        if select_card:
            carte_select = tableau_cartes[coord_card[0]][coord_card[1]]
            if fonctions_generales.check_move(carte_select, carte_pioche, regles_jeu):
                memory_pioche = carte_pioche
                memory_coord = coord_card[0], coord_card[1]
                carte_pioche = tableau_cartes[coord_card[0]][coord_card[1]]
                del(tableau_cartes[coord_card[0]][coord_card[1]])
                allow_redo = True
            select_card = False
            time.sleep(0.2)

        check_end(tableau_cartes, carte_pioche, pioche_cartes, regles_jeu)


def rajoute_carte_vide(cartes_dico):
    cartes_dico["V00.png"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
    return(cartes_dico)
    

def taille_golf(regles):

    if regles == 13:
        colonnes = 7
        lignes = 5
    elif regles == 7:
        colonnes = 6
        lignes = 3
    elif regles == 8:
        colonnes = 6
        lignes = 3
    elif regles == 14:
        colonnes = 6
        lignes = 6
    elif regles == 16:
        colonnes = 7
        lignes = 6
    else:
        colonnes = 7
        lignes = 5

    return(lignes, colonnes)


def check_mouse(mouse, tableau_cartes, nbre_pioche, colonnes, screen_size):

    for i in range(colonnes):
        if len(tableau_cartes[i]) > 0:
            if (i * 120) + 80 <= mouse[0] < (i * 120) + 80 + 75 and ((len(tableau_cartes[i]) - 1) * 50) + 30 <= mouse[1] < ((len(tableau_cartes[i]) - 1) * 50) + 30 + 118:
                return("cartes",i)

    if 80 <= mouse[0] < (nbre_pioche * 5) + 80 + 75 and 400 <= mouse[1] < 400 + 118:
        return("pioche",'')

    return('','')

def check_end(tableau_cartes, carte_pioche, pioche_cartes, regles_jeu):
        ##ENDGAME
        for i in range(len(tableau_cartes)):
            if len(tableau_cartes[i])!=0:
                break
            if i == len(tableau_cartes) - 1:
                end_game('win')

        if len(pioche_cartes) == 0:
            for i in range(len(tableau_cartes)):
                test_coord = (i,-1)
                if len(tableau_cartes[i]) != 0:
                    if fonctions_generales.check_move(tableau_cartes[i][-1], carte_pioche, regles_jeu):
                        break
                if i == len(tableau_cartes) - 1:
                    end_game("loss")


def end_game(outcome):
    print(outcome)
    pygame.quit()
    sys.exit()

def main():
    golf('simpsons',28)



# ==============================================================================
if __name__ == '__main__':
  main()
