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


def napoleon(type_cartes, taille_jeu):
    pygame.init()
    pygame.display.set_caption("MIASHS")

    ##Définition des règles
    regles = int(taille_jeu / 4)
    
    fenetreX, fenetreY = (200+(regles+1)*80, 750)
    fenetre = pygame.display.set_mode((fenetreX, fenetreY))

    ##Chargement des images
    fond = pygame.image.load("images/fond/fond.png")
    fond = pygame.transform.scale(fond, (fenetreX, fenetreY))
    repertoire_cartes = ("images/" + type_cartes + "/cartes/")
    liste_images = fonctions_generales.generation_jeu_aleatoire(repertoire_cartes, regles, 1)
    nombre_cartes = len(liste_images)
    cartes_dico = images(liste_images, type_cartes)
    
    lignes = 4
    colonnes = int(nombre_cartes / lignes)

    ## creation d'une liste de base, et melange de cartes_dico
    liste_cartes = [name for name in cartes_dico] ## prends chaque nom de cartes_dico dans la biblioteque

    ## rajout de cartes_dico vides a la fin des listes.
    cartes_dico = rajoute_carte_vide(cartes_dico)
    for i in range(lignes):
        liste_cartes.append("V00.png")

    shuffle(liste_cartes)
    shuffled = [liste_cartes[x:x + colonnes + 1] for x in range(0, len(liste_cartes), colonnes + 1)] ## cree une liste deux dimensions (lignes * colonnes) avec comme valeur les valeurs de liste_cartes

    ## select transparence
    select1 = pygame.image.load("images/select.png").convert_alpha()
    select2 = pygame.image.load("images/select2.png").convert_alpha()
                

    mouseX, mouseY = (-1,-1)
    select_depart = False ## variable si la carte de depart a été selectionnée
    coord_depart = (-1,-1)
    select_dest = False ## variable si la carte de destination a été selectionnée
    coord_dest = (-1,-1)
    myfont = pygame.font.SysFont("monospace", 20)
    game_started = False ## devient true quand l'utilisateur commence a jouer! (utilise pour les options)
    allow_redo = False ## permet de limiter le nombre de 'redo's de l'utilisateur a une fois
    redo = False ## si l'utilisateur veux revenir en arriere d'un mouvement
    regles_jeu = [regles, "start", "sup", "same_symbol", "ace on empty", "napoleon"]
    all_options = False

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                ## conversion coordonnées brutes en coordonnées tableau
                tableauX, tableauY = (mouseX - 30) // 80, (mouseY - 30) // 118
                if select_depart == False and 0 <= tableauX < colonnes + 1 and 0 <= tableauY < lignes and shuffled[tableauY][tableauX] != "V00.png": ## pour la carte de depart
                    coord_depart = tableauX, tableauY
                    select_depart = True
                ## si l'utilisateur click sur une carte au lieu du vide en deuxieme choix
                elif select_dest == False and 0 <= tableauX < colonnes + 1 and 0 <= tableauY < lignes and shuffled[tableauY][tableauX] != "V00.png":
                    coord_depart = tableauX, tableauY
                    select_depart = True
                elif select_dest == False and 0 <= tableauX < colonnes + 1 and 0 <= tableauY < lignes and shuffled[tableauY][tableauX] == "V00.png": ## pour la position de destination
                    coord_dest = tableauX, tableauY
                    select_dest = True
                elif selection == "menu":
                    principale.main()
                elif selection == "options":
                    type_cartes, restart = options.options(fenetre, type_cartes, taille_jeu, 1, all_options)
                    if restart:
                        napoleon(type_cartes, taille_jeu)
                    repertoire_cartes = "images/" + type_cartes + "/cartes/"
                    cartes_dico = images(liste_images, type_cartes)
                    cartes_dico = rajoute_carte_vide(cartes_dico)
                elif selection == "retour" and allow_redo:
                    redo = True

            elif event.type == KEYDOWN:
                if event.key == K_o:
                    shuffled = cheat_ordonne(shuffled, lignes, colonnes)
                    time.sleep(0.2)


        ## affiche fond
        fenetre.blit(fond, (0,0))

        ## reviens en arriere d'un mouvement
        if redo:
            shuffled[memory_depart[1]][memory_depart[0]] = shuffled[memory_dest[1]][memory_dest[0]]
            shuffled[memory_dest[1]][memory_dest[0]] = "V00.png"
            redo = False
            allow_redo = False
            
        
        ## affiche cartes_dico
        for y in range(lignes):
            for x in range(colonnes + 1): # + 1 pour rajouter la carte vide à la fin de chaque ligne
                fenetre.blit(cartes_dico[shuffled[y][x]], (x * 80 + 30 , y * 118 + 30))

        ## affiche contour carte depart
        if select_depart:
            fenetre.blit(select1, (coord_depart[0] * 80 + 30 , coord_depart[1] * 118 + 30)) ## select transparence

        ## affiche contour emplacement dest
        if select_dest:
            fenetre.blit(select2, (coord_dest[0] * 80 + 30 , coord_dest[1] * 118 + 30)) ## select transparence

        ## affiche les boutons a droite
        selection = fonctions_generales.barre_laterale(fenetre, fenetreX, (mouseX,mouseY))

        pygame.display.flip()

        if select_dest:
            carte_depart = shuffled[coord_depart[1]][coord_depart[0]]
            carte_compare = shuffled[coord_dest[1]][coord_dest[0]-1]
            regles_jeu[4] = coord_dest[0]
            if fonctions_generales.check_move(carte_depart, carte_compare, regles_jeu):
                memory_card = shuffled[coord_depart[1]][coord_depart[0]]
                memory_depart = coord_depart
                memory_dest = coord_dest
                shuffled[coord_dest[1]][coord_dest[0]] = shuffled[coord_depart[1]][coord_depart[0]]
                shuffled[coord_depart[1]][coord_depart[0]] = "V00.png"
                game_started = True ## le jeu a commence
                allow_redo = True
            select_depart,select_dest = False, False
            time.sleep(0.2) ## pour qu'il y ait une ptite pause pour qu'on voit bien les couleurs des contours


        check_end(shuffled, lignes, colonnes, regles)


def cheat_ordonne(shuffled, lignes, colonnes):
    ordered = [[],[],[],[]]
    indice_vide = 0
    for y in range(lignes):
        for x in range(colonnes + 1):
            if shuffled[y][x][0] == "C":
                ordered[0].append(shuffled[y][x])
            elif shuffled[y][x][0] == "D":
                ordered[1].append(shuffled[y][x])
            elif shuffled[y][x][0] == "H":
                ordered[2].append(shuffled[y][x])
            elif shuffled[y][x][0] == "S":
                ordered[3].append(shuffled[y][x])
            elif shuffled[y][x][0] == "V":
                ordered[indice_vide].append(shuffled[y][x])
                indice_vide += 1


                
    ordered[0].sort()
    ordered[1].sort()
    ordered[2].sort()
    ordered[3].sort()
    
    return(ordered)


def rajoute_carte_vide(cartes_dico):
    cartes_dico["V00.png"] = pygame.image.load("images/carte_vide/V00.png").convert_alpha()
    return(cartes_dico)


def check_end(shuffled, lignes, colonnes, regles): #### A VERIFIER

## si le jeu est perdu
    dead_end = 0
    for y in range(lignes):
        for x in range(colonnes + 1):
            if shuffled[y][x] == "V00.png":
                if int(shuffled[y][x - 1][1:3]) == 13:
                    dead_end += 1
                elif shuffled[y][x - 1] == "V00.png":
                    dead_end += 1
    if dead_end == 4:
        end_game("loss")

## si le jeu est gagne
    temp = 0
    break_loop = False
    num1 = 0
    num2 = 0
    type1 = ""
    type2 = ""

    ordre = fonctions_generales.ordre_valeurs(regles, "start")
        
    for y in range(lignes):
        for x in range(colonnes - 1): # -1 pour pouvoir comparer un a un
##            les try except permettent d'eliminer l'erreur ou il regarde les cases vides (parce que num_casesvides = 0 et 0 pas dans ordre)
            try:
                num1 = ordre.index(int(shuffled[y][x][1:3]))
            except ValueError:
                num1 = -1
            try:
                num2 = ordre.index(int(shuffled[y][x+1][1:3]))
            except ValueError:
                num2 = -1
            type1 = shuffled[y][x][0]
            type2 = shuffled[y][x+1][0]
            if not (type1 == type2 and (num1 + 1) == num2):
                return
    end_game("win")


def end_game(outcome):
    print(outcome)
    pygame.quit()
    sys.exit()

def main():
    napoleon('simpsons',52)


# ==============================================================================
if __name__ == '__napoleon__':
  napoleon()
