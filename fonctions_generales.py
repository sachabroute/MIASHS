import pygame
import pickle
from pygame.locals import *
import sys
import os
import time
from random import *

############################################################################################
############################################################################################
############################################################################################

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

    ##Définition de l'ordre de valeur des cartes selon leur numéro de fichier :
    ##15 et 16 correspondent au 11 et au 12, et 14 au cavalier.
    ordre_valeurs_cartes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16, 11, 14, 12, 13]

    ##Définition de la priorité dans laquelle les cartes seront prises selon le nombre
    ##de cartes demandées dans le jeu.
    ordre_priorite_cartes = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 14, 15, 16]

    ##Variable de sortie
    ordre_selon_regles = []

    ##On prend uniquement les cartes dont on a besoin : si on joue avec 8 cartes, on prend
    ##les 8 premières valeurs de ordre_priorite_cartes, c'est à dire les cartes du 7 au 10,
    ##le valet, la reine, le roi et l'as.
    ordre_priorite_cartes = ordre_priorite_cartes[0:nombre_cartes]

    ##Tri des cartes choisi dans leur ordre de valeurs.
    ##Si on prend 14 cartes, cela permet de placer le cavalier entre le valet et la reine.
    for i in range(len(ordre_valeurs_cartes)) :
        if ordre_valeurs_cartes[i] in ordre_priorite_cartes :
            ordre_selon_regles.append(ordre_valeurs_cartes[i])

    ##Place de l'as dans le jeu. Par défaut il est avant le 2. Si on veut le placer après
    ##le roi, il faut que "place_as" soit égal à "end".
    if 1 in ordre_selon_regles and place_as == "end" :
        ordre_selon_regles.insert(nombre_cartes-1, ordre_selon_regles.pop(0))

    ##On renvoie l'ordre des cartes.
    return(ordre_selon_regles)

############################################################################################
############################################################################################
############################################################################################

def check_move(carte_depart, carte_compare, regles) :
    ##Renvoie Vrai ou Faux selon que la carte sélectionnée peut etre placée sur/après
    ##la carte visée, selon la liste regles :
    ##regles = [nombre_cartes, place_as, corresp_number, corresp_color, first_card]
    
    ####nombre_cartes : nombre de cartes dans le jeu.
    ####Prend les valeurs 7, 8, 13, 14 ou 16.
    
    ####place_as : place de l'as, avant le 2 ou après le K.
    ####Prend les valeurs : "start" ou "end".
    
    ####corresp_number : vérifie si la différence que doit avoir la carte_depart
    ####avec la carte_compare. Si on veut placer un 6 sur un 7, la carte_compare
    ####est donc inférieure à la carte_depart, on utilise "inf".
    ####Prend les valeurs : "inf", "sup", "same" ou "both".
    
    ####corresp_color : vérifie la couleur que peut prendre la carte_compare
    ####pour qu'elle vérifie la règle du jeu.
    ####Prend les valeurs : "same_symbol", "same_color", "diff_color" ou "any".
    
    ####first_card : vérifie quelle carte on peut placer sur un emplacement vide.
    ####Prend les valeurs : "king" ou "ace".

    ##Par défaut, on considère que tout est faux afin de ne pas valider le mouvement.
    valid_number = False
    valid_color = False
    valid = False

    ##Récupère l'ordre des cartes avec la fonction ordre_valeurs.
    ordre_selon_regles = ordre_valeurs(regles[0], regles[1])

    ##On place un "0" dans ordre_selon_regles pour définir quelle carte se place sur
    ##un emplacement vide.
    if regles[4] == "king" :
        ordre_selon_regles.append(0)
    elif regles[4] == "ace" :
        ordre_selon_regles.insert(0, 0)

    ##Récupération du symbole (C, D, H, S) et du numéro de la carte de départ.
    type_carte_depart = carte_depart[0]
    num_carte_depart = int(carte_depart[1:3])

    ##Récupération du symbole (C, D, H, S) et du numéro de la carte comparée.
    type_carte_compare = carte_compare[0]
    num_carte_compare = int(carte_compare[1:3])

    ##On soustrait les numéros de la carte comparée à la carte de départ.
    try:
        compare = ordre_selon_regles.index(num_carte_depart) - ordre_selon_regles.index(num_carte_compare)
    except ValueError:
        compare = -100

    ##Définition de listes correspondant aux possibilités de différences entre les cartes.
    corresp_number = {"inf" : [-1], "sup" : [1], "same" : [0], "both" : [-1,1], "both+" : [-1,1,regles[0]-1,-(regles[0]-1)] }

    ##Création des variables red et black permettant de vérifier si une carte est rouge
    ##(carreau ou coeur) ou noire (trèfle ou pique).
    red = ["D", "H"]
    black = ["C", "S"]

    ##Création des variables color1 correspondant à la même couleur que la carte de départ,
    ##et de color2 correspondant à la couleur opposée.
    if type_carte_depart in red :
        color1 = red
        color2 = black
    else :
        color1 = black
        color2 = red

    ##Définition de listes correspondant aux possibilités de couleur de la carte_compare.        
    corresp_color = {"same_symbol" : [type_carte_depart], "same_color" : color1, "diff_color" : color2, "any" : ["C", "D", "H", "S"]}

    ##Vérification de la validité du numéro.
    if compare in corresp_number[regles[2]] :
        valid_number = True

    ##Vérification de la validité de la couleur.
    if type_carte_compare in corresp_color[regles[3]] or type_carte_compare == "V" :
        valid_color = True

    ##Vérification de la validité du déplacement.
    if (valid_number == True and valid_color == True):
        valid = True

    ## pour le napoleon si il y a >= 2 emplacements vides cote a cote
    if carte_compare == "V00.png" and num_carte_depart != ordre_selon_regles[0] and regles[5] == "napoleon":
        valid = True
        
    if num_carte_depart == ordre_selon_regles[0] and regles[4] == 0:
        valid = True


    ##Retour de la validité du déplacement : True ou False.
    return(valid)

############################################################################################
############################################################################################
############################################################################################

def generation_jeu_aleatoire(repertoire_cartes, nombre_cartes, nombre_paquets) :
    ##Renvoie un jeu aléatoire en fonction du nombre de cartes dans le paquet
    ##et du nombre de paquets.
    
    ##Récupération des noms des fichiers images dans le répertoire correspondant
    liste_images_brutes = os.listdir(repertoire_cartes)

    ##Variable de sortie
    liste_images_regles = []

    ##Chargement des cartes i fois, selon le nombre de paquets utilisé
    for i in range(nombre_paquets) :

        ##Enregistrement de j cartes, selon le nombre de cartes dans un paquet
        for j in range(len(liste_images_brutes)) :            

            #On prend du caractère [1] au caractère [2] pour avoir le numéro de carte
            cardnumber = liste_images_brutes[j][1:3]

            ##On récupère la liste des cartes utilisées (on ne prend pas le cavalier
            ##quand on a 13 cartes, par exemple)
            liste_cartes = ordre_valeurs(nombre_cartes, "end")  

            ##On ajoute la carte uniquement si elle est dans la liste. Le try
            ##permet de ne pas prendre les fichiers temp
            try :
                if int(cardnumber) in liste_cartes :
                    liste_images_regles.append(liste_images_brutes[j])

            except :
                pass

    ##On mélange la liste pour générer un jeu aléatoire
    shuffle(liste_images_regles)

    ##Retour de la liste
    return(liste_images_regles)

############################################################################################
############################################################################################
############################################################################################

def images(repertoire_cartes) :
    ##Renvoie un dictionnaire d'images en fonction des noms de cartes.

    ##Récupération des cartes et placement dans une liste
    liste_images_brutes = os.listdir(repertoire_cartes)

    ##Définition de la variable de sortie
    dico_images = {}

    ##On place le chargement pygame en face de chaque image "X##.png". Le try permet de
    ##ne pas prendre en compte les fichiers temp.
    for i in range(len(liste_images_brutes)) :
        try :
            dico_images[liste_images_brutes[i]] = pygame.image.load(repertoire_cartes+liste_images_brutes[i]).convert_alpha()
        except :
            pass

    ##Renvoi du dictionnaire en sortie
    return(dico_images)

############################################################################################
############################################################################################
############################################################################################

def barre_laterale(fenetre, fenetreX, mouse_coord) :
    dico_images_barre = images("images/options/")
    selection = ""

    fenetre.blit(dico_images_barre["menu_off.png"], (fenetreX-50,50))
    fenetre.blit(dico_images_barre["options_off.png"], (fenetreX-50,100))
    fenetre.blit(dico_images_barre["retour_off.png"], (fenetreX-50,150))

    if fenetreX-50 < mouse_coord[0] < fenetreX-20 and 50 < mouse_coord[1] < 80 :
        fenetre.blit(dico_images_barre["menu_on.png"], (fenetreX-50,50))
        selection = "menu"
    if fenetreX-50 < mouse_coord[0] < fenetreX-20 and 100 < mouse_coord[1] < 130 :
        fenetre.blit(dico_images_barre["options_on.png"], (fenetreX-50,100))
        selection = "options"
    if fenetreX-50 < mouse_coord[0] < fenetreX-20 and 150 < mouse_coord[1] < 180 :
        fenetre.blit(dico_images_barre["retour_on.png"], (fenetreX-50,150))
        selection = "retour"

    return(selection)
        
############################################################################################
############################################################################################
############################################################################################
