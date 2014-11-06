from random import *

## D(diamonds) H(hearts) S(spades) C(clubs)
cartes = ["1 d","2 d","3 d","4 d","5 d","6 d","7 d","8 d","9 d","10 d","11 d","12 d","13 d",
          "1 h","2 h","3 h","4 h","5 h","6 h","7 h","8 h","9 h","10 h","11 h","12 h","13 h",
          "1 s","2 s","3 s","4 s","5 s","6 s","7 s","8 s","9 s","10 s","11 s","12 s","13 s",
          "1 c","2 c","3 c","4 c","5 c","6 c","7 c","8 c","9 c","10 c","11 c","12 c","13 c"]

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
