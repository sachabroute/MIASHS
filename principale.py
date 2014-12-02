import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.display.set_caption("MIASHS")

fenetre = pygame.display.set_mode((1020, 720))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
