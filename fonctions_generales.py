import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
from random import *

def ordre_valeurs(nombre_cartes, place_as) :
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

def check_move(carte_depart, carte_compare, regles) :
    ##Renvoie Vrai ou Faux selon que la carte sélectionnée peut etre placée sur/après
    ##la carte visée, selon :
    ##
    ##ordre_jeu : sup si la carte sélectionnée doit être de valeur supérieure
    ##(ex. Napoleon), inf si elle doit etre de valeur inférieure
    ##(ex. Solitaire), same si elle doit être égale. Si elle doit être les deux,
    ##il suffit de faire un test pour "sup" et pour "inf" (ex. Golf)
    ##
    ##color_jeu : same si elle doit être de même symbole (ex. Napoleon),
    ##same_color si elle doit être de même couleur, et diff_color si elle
    ##doit être de couleur différente (ex. Solitaire).

    valid_number = False
    valid_color = False
    valid = False
    
    ordre_selon_regles = ordre_valeurs(regles[0], regles[1])
    
    type_carte_depart = carte_depart[0]
    num_carte_depart = int(carte_depart[1:3])
    type_carte_compare = carte_compare[0]
    num_carte_compare = int(carte_compare[1:3])
    
    compare = ordre_selon_regles.index(num_carte_depart)-ordre_selon_regles.index(num_carte_compare)
    corresp_number = {"sup" : [-1], "inf" : [1], "same" : [0], "both" : [-1,1] }

    red = ["D", "H"]
    black = ["C", "S"]
    
    if type_carte_depart in red :
        color1 = red
        color2 = black
    else :
        color1 = black
        color2 = red
    corresp_color = {"same_symbol" : [type_carte_depart], "same_color" : color1, "diff_color" : color2, "any" : ["C", "D", "H", "S"]}

    if compare in corresp_number[regles[2]] :
        valid_number = True

    if type_carte_compare in corresp_color[regles[3]] :
        valid_color = True

    if valid_number == True and valid_color == True :
        valid = True
    
    return(valid)

def generation_jeu_aleatoire(repertoire_cartes, nombre_cartes, nombre_paquets) :
    ##Génère un jeu aléatoire
    liste_images_brutes = os.listdir(repertoire_cartes)
    liste_images_regles = []

    for i in range(nombre_paquets) :
        for j in range(len(liste_images_brutes)) :
            cardsplit = liste_images_brutes[j] #On prend du caractère [1] au caractère [2] pour avoir le numéro de carte.
            cardnumber = cardsplit[1:3]
            liste_cartes = ordre_valeurs(nombre_cartes, "end")

            try :
                if int(cardnumber) in liste_cartes : ##Si ce numéro est inférieur au nombre dans règles, alors on append, sinon rien.
                    liste_images_regles.append(liste_images_brutes[j])

            except :
                pass

    shuffle(liste_images_regles)

    return(liste_images_regles)

def images(repertoire_cartes) :
    os.chdir(repertoire_cartes)
    liste_images_brutes = os.listdir()
    dico_images = {}
    
    for i in range(len(liste_images_brutes)) :
        try :
            dico_images[liste_images_brutes[i]] = pygame.image.load(liste_images_brutes[i]).convert_alpha()
        except :
            pass
    return(dico_images)
