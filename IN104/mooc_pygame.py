#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *

#Initialisation de la bibliothèque Pygame
pygame.init()

#Création de la fenêtre
fenetre = pygame.display.set_mode((640,480), RESIZABLE)

fond = pygame.image.load("background.jpg").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso = pygame.image.load("mushroom.png").convert_alpha()
perso = pygame.transform.scale(perso,[100,100])
position_perso = perso.get_rect()
fenetre.blit(perso, position_perso)


#Rafraîchissement de l'écran
pygame.display.flip()



pygame.key.set_repeat(400, 30)


#BOUCLE INFINIE
continuer = 1
while continuer:
    for event in pygame.event.get():	#Attente des événements
        if event.type == QUIT:
            continuer = 0
        if event.type == KEYDOWN:
            if event.key == K_DOWN:	#Si "flèche bas"
                position_perso = position_perso.move(0,3)
            if event.key == K_UP:
                position_perso = position_perso.move(0,-3)
            if event.key == K_RIGHT:
                position_perso = position_perso.move(3,0)
            if event.key == K_LEFT:
                position_perso = position_perso.move(-3,0)

    #Re-collage
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, position_perso)
	#Rafraichissement
    pygame.display.flip()





pygame.quit()
