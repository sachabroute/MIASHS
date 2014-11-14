from random import shuffle
import pygame
import pickle
import sys
from images import *
from pygame.locals import *
pygame.init()
pygame.display.set_caption("MIASHS")

fenetre = pygame.display.set_mode((1175, 750), RESIZABLE)
pygame.key.set_repeat(1175, 750)

def generation_liste() :
    
    ##Génération d'une liste de cartes aléatoire
    liste_cartes = []
    liste_melangee = []
    liste_couleurs = ["H", "D", "S", "C"]
    liste_numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K"]
    
    for i in range(0,4) :
        
        for j in range(0,13) :
            carte = liste_numeros[j]+" "+liste_couleurs[i]
            liste_cartes.append(carte)
            liste_melangee.append(carte)            

    print("Liste de cartes :\n", liste_cartes,"\n")

    shuffle(liste_melangee)
    
    print("Liste aléatoire :\n", liste_cartes, "\n")

    ##Création du plateau de jeu
    plateau = []

    for i in range(0,4) :
        ligne = liste_melangee[i*13:(i*13)+13]
        ligne.append(" ")
        plateau.append(ligne)
        ligne = []

    print("Plateau de jeu :\n", plateau)

    return(plateau, liste_cartes)
    
def affichage_jeu(plateau, liste_cartes) :

    background_virgin = pygame.Surface(fenetre.get_size())
    background_virgin = fenetre.convert()
    background_virgin.fill((0, 0, 0)) ##Remplissage de l'arrière plan en noir
    C1 = pygame.image.load(image_C1).convert_alpha()
    C2 = pygame.image.load(image_C2).convert_alpha()
    C3 = pygame.image.load(image_C3).convert_alpha()
    C4 = pygame.image.load(image_C4).convert_alpha()
    C5 = pygame.image.load(image_C5).convert_alpha()
    C6 = pygame.image.load(image_C6).convert_alpha()
    C7 = pygame.image.load(image_C7).convert_alpha()
    C8 = pygame.image.load(image_C8).convert_alpha()
    C9 = pygame.image.load(image_C9).convert_alpha()
    C10 = pygame.image.load(image_C10).convert_alpha()
    CJ = pygame.image.load(image_CJ).convert_alpha()
    CQ = pygame.image.load(image_CQ).convert_alpha()
    CK = pygame.image.load(image_CK).convert_alpha()
    D1 = pygame.image.load(image_D1).convert_alpha()
    D2 = pygame.image.load(image_D2).convert_alpha()
    D3 = pygame.image.load(image_D3).convert_alpha()
    D4 = pygame.image.load(image_D4).convert_alpha()
    D5 = pygame.image.load(image_D5).convert_alpha()
    D6 = pygame.image.load(image_D6).convert_alpha()
    D7 = pygame.image.load(image_D7).convert_alpha()
    D8 = pygame.image.load(image_D8).convert_alpha()
    D9 = pygame.image.load(image_D9).convert_alpha()
    D10 = pygame.image.load(image_D10).convert_alpha()
    DJ = pygame.image.load(image_DJ).convert_alpha()
    DQ = pygame.image.load(image_DQ).convert_alpha()
    DK = pygame.image.load(image_DK).convert_alpha()
    H1 = pygame.image.load(image_H1).convert_alpha()
    H2 = pygame.image.load(image_H2).convert_alpha()
    H3 = pygame.image.load(image_H3).convert_alpha()
    H4 = pygame.image.load(image_H4).convert_alpha()
    H5 = pygame.image.load(image_H5).convert_alpha()
    H6 = pygame.image.load(image_H6).convert_alpha()
    H7 = pygame.image.load(image_H7).convert_alpha()
    H8 = pygame.image.load(image_H8).convert_alpha()
    H9 = pygame.image.load(image_H9).convert_alpha()
    H10 = pygame.image.load(image_H10).convert_alpha()
    HJ = pygame.image.load(image_HJ).convert_alpha()
    HQ = pygame.image.load(image_HQ).convert_alpha()
    HK = pygame.image.load(image_HK).convert_alpha()
    S1 = pygame.image.load(image_S1).convert_alpha()
    S2 = pygame.image.load(image_S2).convert_alpha()
    S3 = pygame.image.load(image_S3).convert_alpha()
    S4 = pygame.image.load(image_S4).convert_alpha()
    S5 = pygame.image.load(image_S5).convert_alpha()
    S6 = pygame.image.load(image_S6).convert_alpha()
    S7 = pygame.image.load(image_S7).convert_alpha()
    S8 = pygame.image.load(image_S8).convert_alpha()
    S9 = pygame.image.load(image_S9).convert_alpha()
    S10 = pygame.image.load(image_S10).convert_alpha()
    SJ = pygame.image.load(image_SJ).convert_alpha()
    SQ = pygame.image.load(image_SQ).convert_alpha()
    SK = pygame.image.load(image_SK).convert_alpha()
    fond = pygame.image.load(image_fond).convert_alpha()

    ok = True

    print(plateau)
    
    while ok :
        for event in pygame.event.get() :

            ##Blit du fond
            fenetre.blit(background_virgin, (0, 0))
            background_virgin.blit(fond, (0, 0))

            liste_variables = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, CJ, CQ, CK,
                               D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, DJ, DQ, DK,
                               H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, HJ, HQ, HK,
                               S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, SJ, SQ, SK]

            for i in range(4) :
                for j in range(13) :
                    for k in range(52) :
                        if plateau[i][j] == liste_cartes[k] :
                            fond.blit(liste_variables[k], (j*80+30, i*118+30))

        pygame.display.flip()
        ok = False

def main() :
    plateau, liste_cartes = generation_liste()
    affichage_jeu(plateau, liste_cartes)

if __name__ == "__main__" :
    main()
    
