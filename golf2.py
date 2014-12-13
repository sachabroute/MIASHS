import pygame
from pygame.locals import *
import sys
import os
import time
from random import *
import game_options

def ordre_valeurs(nombre_cartes, place_as):
    ##Renvoie automatiquement une liste d'ordre des valeurs, selon le nombre de
    ##cartes dans les règles. Fonctionne pour nombre_cartes = 7, 8, 13, 14 et 16 :
    ##Jeu de 28 cartes (4*7) : 7, 8, 9, 10, J, Q, K
    ##Jeu de 32 cartes (4*8) : 1, 7, 8, 9, 10, J, Q, K
    ##Jeu de 52 cartes (4*13) : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
    ##Jeu de 56 cartes (4*14) : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, C, Q, K
    ##Jeu de 64 cartes (4*16) : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, J, C, Q, K
    ##La variable place_as permet de définir si le 1 doit se trouver au début ou
    ##à la fin du paquet.

    ordre_valeurs_cartes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 11, 14, 12, 13]
    ordre_priorite_cartes = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 14, 15, 16]
    ordre_selon_regles = []

    ordre_priorite_cartes = ordre_priorite_cartes[0:nombre_cartes]

    for i in range(len(ordre_valeurs_cartes)) :
        if ordre_valeurs_cartes[i] in ordre_priorite_cartes :
            ordre_selon_regles.append(ordre_valeurs_cartes[i])

    if 1 in ordre_selon_regles and place_as == "end" :
        ordre_selon_regles.insert(nombre_cartes-1, ordre_selon_regles.pop(0))
        
    return(ordre_selon_regles)

def chargement_images(type_cartes, regles):

    ordre = ordre_valeurs(regles, "start")

    ##Chargement des cartes
    liste_images_brutes = os.listdir("images/" + type_cartes + "/cartes/") ##Insère toutes les images du répertoire dans une liste
    liste_images_regles = [] ##Nouvelle liste qui contiendra uniquement les images de jeu

    ##Boucle supprimant les cartes cavalier si égal à 13
    for i in range(len(liste_images_brutes)) :
        cardsplit = liste_images_brutes[i] #On prend du caractère [1] au caractère [2] pour avoir le numéro de carte.
        cardnumber = cardsplit[1:3]
        if int(cardnumber) in ordre : ##Si ce numéro est inférieur au nombre dans règles, alors on append, sinon rien.
            liste_images_regles.append(liste_images_brutes[i])

    ##Fin du chargement des images
    nombre_cartes = int(len(liste_images_regles)) ##Définit le nombre de cartes à partir de la taille de la liste
    
    return(liste_images_regles, nombre_cartes)

def chargement_dico(type_cartes, regles):

    ##chargement des cartes
    liste_images_regles, nombre_cartes = chargement_images(type_cartes, regles)
    
    cartes = {} ## initialisation biblioteque vide
    
    for i in range(nombre_cartes):
        indice = liste_images_regles[i].split(".")[0] ## correspond au nom de chaque carte. on split pour enlever le '.png', on se retrouve avec 'C01', 'C02', etc...
        cartes["%s" %(indice)] = pygame.image.load("images/" + type_cartes + "/cartes/"+liste_images_regles[i]).convert_alpha()
    #### end load images (wouaaah c'est super court t'as vu!??)

    return(cartes)

def rajoute_carte_vide(cartes):
    cartes["V00"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
    return(cartes)
    

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



def golf(type_cartes, taille_jeu):
    pygame.init()
    pygame.display.set_caption("MIASHS")



    ##Définition des règles
    regles = int(taille_jeu / 4)
## a voir si on peut changer les lignes et colonnes par la suite
    lignes, colonnes = taille_golf(regles)
##    fenetre = pygame.display.set_mode((60+(regles+1)*80, 750))
    fenetreX, fenetreY = 80+(colonnes*75)+((colonnes-1)*45)+80, 750
    fenetre = pygame.display.set_mode((fenetreX, fenetreY))

    ##Chargement des images
    fond = pygame.image.load("images/fond/fond.png")
    fond = pygame.transform.scale(fond, (fenetreX, fenetreY))

    options = pygame.image.load("images/options/rouage.png")
    options_select = pygame.image.load("images/options/rouage_select.png")
    
    cartes = chargement_dico(type_cartes, regles)


    ## creation d'une liste de base, et melange de cartes
    liste_cartes = [name for name in cartes]
    shuffle(liste_cartes)
    tableau_cartes = [liste_cartes[x:x+lignes] for x in range(0, colonnes * lignes, lignes)]
    pioche_cartes = liste_cartes[colonnes * lignes:]
    poubelle_cartes = []

    ## le dos des cartes (pour la pioche), carte vide
    dos = pygame.image.load("images/" + type_cartes + "/dos/dos.png").convert_alpha()
    cartes = rajoute_carte_vide(cartes)
    carte_pioche = "V00"
    

    mouseX, mouseY = (-1,-1)
    select_card = False
    coord_card = (-1,-1)
    pioche = False
    myfont = pygame.font.SysFont("monospace", 20)
    game_started = False ## dans les options, permet de savoir si l'utilisateur peut changer la taille ou non
    allow_redo = False ## permet de limiter le nombre de 'redo's de l'utilisateur a une fois
    redo = False ## si l'utilisateur veux revenir en arriere d'un mouvement
    last_move = '' ## prends les valeurs 'pioche' ou 'tableau' pour indiquer le dernier type de mouvement de l'utilisateur

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                click_type, ind = check_mouse((mouseX, mouseY), tableau_cartes, len(pioche_cartes), colonnes, (fenetreX, fenetreY))
                if click_type == "cartes" and carte_pioche != "V00":
                    coord_card = (mouseX - 80) // 120, len(tableau_cartes[ind]) - 1
                    select_card = True
                    game_started = True
                    last_move = click_type
                elif click_type == "pioche":
                    memory_pioche = carte_pioche
                    carte_pioche = pioche_cartes.pop()
                    game_started = True
                    allow_redo = True
                    last_move = click_type
                elif click_type == "options":
                    type_cartes, taille_jeu, restart = game_options.options(fenetre, type_cartes, taille_jeu, game_started)
                    if restart:
                        golf(type_cartes, taille_jeu)
                    cartes = chargement_dico(type_cartes, regles)
                    cartes = rajoute_carte_vide(cartes)
                elif allow_redo and click_type == "voyage temporel":
                    start_time = pygame.time.get_ticks()
                    redo = True

            elif event.type == KEYDOWN:
                if event.key == K_p:
                    print(ordre_valeurs(regles, "start"))

        ## affiche fond
        fenetre.blit(fond, (0,0))

        ## affiche rouage options
        fenetre.blit(options, (fenetreX - 50, 15))
        ## affiche rouage selectionne
        if fenetreX - 50 <= mouseX <= fenetreX - 20 and 15 <= mouseY <= 45:
            fenetre.blit(options_select, (fenetreX - 50, 15))

        ## affiche retour en arriere d'un mouvement
        if allow_redo:
            pygame.draw.rect(fenetre, (150,100,150), (500, 400, 410, 50), 0)
            if 500 <= mouseX <= 910 and 400 <= mouseY <= 450:
                pygame.draw.rect(fenetre, (100,150,150), (500, 400, 410, 50), 0)
        else:
            pygame.draw.rect(fenetre, (150,150,150), (500, 400, 410, 50), 0)
        label = myfont.render("Revenir en arriere d'un mouvement", 1, (230,230,230))
        fenetre.blit(label, (505, 410))

## reviens en arriere d'un pas
        if redo:
            pygame.draw.rect(fenetre, (randrange(0,255),randrange(0,255),randrange(0,255)), (500, 400, 410, 50), 0)
            if abs(pygame.time.get_ticks() - start_time) > 1000 and last_move == 'cartes':
                tableau_cartes[memory_coord[0]].append(carte_pioche)
                carte_pioche = memory_pioche
                redo = False
                allow_redo = False
            elif abs(pygame.time.get_ticks() - start_time) > 1000 and last_move == 'pioche':
                pioche_cartes.append(carte_pioche)
                carte_pioche = memory_pioche
                redo = False
                allow_redo = False

        
        ## affiche cartes
        for x in range(colonnes):
            for y in range(lignes):
                try:
                    fenetre.blit(cartes[tableau_cartes[x][y]], (x * 120 + 80, y * 50 + 30))
                except:
                    break

        ## affiche pioche
        for i in range(len(pioche_cartes)):
            fenetre.blit(dos, (80 + i * 5, 400))

        ## affiche contour carte (+ 1 pour colonnes pour la colonne vide du depart)
        if select_card == True:
            pygame.draw.rect(fenetre, (0, 255, 0), ((coord_card[0] * 120 + 80 , coord_card[1] * 50 + 30), (75 , 113)), 3)


        fenetre.blit(cartes[carte_pioche], (300, 400))

        pygame.display.flip()

        if select_card:
            if check_move(tableau_cartes, carte_pioche, coord_card, regles):
                memory_pioche = carte_pioche
                memory_coord = coord_card[0], coord_card[1]
                carte_pioche = tableau_cartes[coord_card[0]][coord_card[1]]
                del(tableau_cartes[coord_card[0]][coord_card[1]])
                allow_redo = True
            select_card = False
            time.sleep(0.3)

        ##ENDGAME
        for i in range(len(tableau_cartes)):
            if len(tableau_cartes[i])!=0:
                break
            if i == len(tableau_cartes) - 1:
                end_game('win')

        
##        FIGURE OUT HOW TO DEAL WITH LOSING THE GAME
##        if len(pioche_cartes) == 0 and len(tableau_cartes) > 1:
##            end_game('loss')

        if len(pioche_cartes) == 0:
            for i in range(len(tableau_cartes)):
                test_coord = (i,-1)
                if len(tableau_cartes[i]) != 0:
                    if check_move(tableau_cartes, carte_pioche, test_coord, regles):
                        break
                if i == len(tableau_cartes) - 1:
                    end_game("loss")
                    
        
        ##reset variables
        mouseX, mouseY = (-1,-1)


def check_move(tableau_cartes, carte_pioche, coord_card, regles):
    ordre = ordre_valeurs(regles, "start")

    valid = False
    num_carte = int(tableau_cartes[coord_card[0]][coord_card[1]][1:3])
    num_carte_pioche = int(carte_pioche[1:3])

    compare = abs(ordre.index(num_carte) - ordre.index(num_carte_pioche))
    print(compare)
    if compare == 1:
        valid = True
    elif 1 in ordre and ordre.index(num_carte) == regles - 1 and ordre.index(num_carte_pioche) == 0: ### roi sur as
        valid = True
    elif 1 in ordre and ordre.index(num_carte) == 0 and ordre.index(num_carte_pioche) == regles - 1: ### as sur roi
        valid = True
    
    return(valid)


def check_mouse(mouse, tableau_cartes, nbre_pioche, colonnes, screen_size):

    for i in range(colonnes):
        if len(tableau_cartes[i]) > 0:
            if (i * 120) + 80 <= mouse[0] < (i * 120) + 80 + 75 and ((len(tableau_cartes[i]) - 1) * 50) + 30 <= mouse[1] < ((len(tableau_cartes[i]) - 1) * 50) + 30 + 118:
                return("cartes",i)

    if 80 <= mouse[0] < (nbre_pioche * 5) + 80 + 75 and 400 <= mouse[1] < 400 + 118:
        return("pioche",'')
    elif screen_size[0] - 50 <= mouse[0] <= screen_size[0] - 20 and 15 <= mouse[1] <= 45:
        return("options",'')
    elif 500 <= mouse[0] <= 910 and 400 <= mouse[1] <= 450:
        return("voyage temporel",'')

    return('','')


def end_game(outcome):
    print(outcome)
    pygame.quit()
    sys.exit()

def main():
    golf('simpsons',52)



# ==============================================================================
if __name__ == '__main__':
  main()
