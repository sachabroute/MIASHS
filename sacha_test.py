from random import *

## D(diamonds) H(hearts) S(spades) C(clubs)
cartes = ["1 D","2 D","3 D","4 D","5 D","6 D","7 D","8 D","9 D","10 D","11 D","12 D","13 D",
          "1 H","2 H","3 H","4 H","5 H","6 H","7 H","8 H","9 H","10 H","11 H","12 H","13 H",
          "1 S","2 S","3 S","4 S","5 S","6 S","7 S","8 S","9 S","10 S","11 S","12 S","13 S",
          "1 C","2 C","3 C","4 C","5 C","6 C","7 C","8 C","9 C","10 C","11 C","12 C","13 C"]

## le jeux de cartes aleatoire est genere dans un tableau 2D avec des espaces a la fin
shuffled = [[" " for i in range(14)] for i in range(4)]
for y in range(4):
    count = 0
    while count < 13:
        card = choice(cartes)
        if card not in shuffled:
            shuffled[y][count] = card
            count += 1


######### PRINT TEST ##########
for i in range(4):
    print(shuffled[i])
###############################

## on demande quel cartes l'utilisateur souhaite deplacer et ou
carte_depart = input("Quelle carte souhaitez-vous deplacer? (numero couleur): ")
carte_dest = input("Ou souhaitez-vous la poser? (pour le moment mets les "
                   "coordonnees du le tableau (x,y) : ")



########## PROBLEMS ###################
## verification de si le coup est permis
print(carte_dest)
coords = ",".split(carte_dest)
print(coords)
coords[0] = int(coords[0])
coords[1] = int(coords[1])
carte_depart = " ".split(carte_depart)

if coords[0] > 0:
    carte_comp = " ".split(shuffled[coords[1]][coords[0]-1])

    if (carte_depart[1] == carte_comp[1]) and (carte_depart[0] == carte_comp[0] + 1):
        print("le coup est permis")
    else:
        print("le coup n'est pas permis")

########################################
