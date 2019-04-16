#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Jeu PacMan
Jeu dans lequel on doit déplacer pacman pour qu'il mange tous les hots-dogs tout en évitant les fantômes 

Script Python
Fichiers : pacman.py, classes.py, constantes.py, n1, n2 + images
"""
import random 
import pygame
from pygame.locals import *

from classes import *
from constantes import *

pygame.init()

#Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))
#Icone
icone = pygame.image.load(image_icone).convert_alpha()
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption(titre_fenetre)

pygame.key.set_repeat(300, 30) #permet de rendre le déplacement continu (delay,interval)
#BOUCLE PRINCIPALE
continuer = 1
while continuer:
	#Chargement et affichage de l'écran d'accueil
	accueil = pygame.image.load(image_accueil).convert()
	fenetre.blit(accueil, (50,0))

	#Rafraichissement
	pygame.display.flip()

	#On remet ces variables à 1 à chaque tour de boucle
	continuer_jeu = 1
	continuer_accueil = 1

	#BOUCLE D'ACCUEIL
	while continuer_accueil:

		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(30)

		for event in pygame.event.get():

			#Si l'utilisateur quitte, on met les variables
			#de boucle à 0 pour n'en parcourir aucune et fermer
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continuer_accueil = 0
				continuer_jeu = 0
				continuer = 0
				#Variable de choix du niveau
				choix = 0

			elif event.type == KEYDOWN:
				#Lancement du niveau 1
				if event.key == K_a:
					continuer_accueil = 0	#On quitte l'accueil
					choix = 'n1'		#On définit le niveau à charger
				#Lancement du niveau 2
				elif event.key == K_b:
					continuer_accueil = 0
					choix = 'n2'



	#on vérifie que le joueur a bien fait un choix de niveau
	#pour ne pas charger s'il quitte
	if choix != 0:
		#Chargement du fond
		fond = pygame.image.load(image_fond).convert()
		fenetre.blit(fond, (0,0))
		pygame.display.flip()


		#Génération d'un niveau à partir d'un fichier
		niveau = Niveau(choix)
		niveau.generer()
		niveau.afficher(fenetre)


		#Création de pac man
		pc = Perso("droite.jpeg", "gauche.jpeg",
		"haut.jpeg", "bas.jpeg", niveau)
		ghost = Ghost("ghost.png","ghost.png","ghost.png","ghost.png",niveau)
		listepos=[] #liste des positions par lesquelles est passé pac man 

	#BOUCLE DE JEU
	while continuer_jeu:

		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(30)

		for event in pygame.event.get():

			#Si l'utilisateur quitte, on met la variable qui continue le jeu
			#ET la variable générale à 0 pour fermer la fenêtre
			if event.type == QUIT:
				continuer_jeu = 0
				continuer = 0

			elif event.type == KEYDOWN:
				#Si l'utilisateur presse Echap ici, on revient seulement au menu
				if event.key == K_ESCAPE:
					continuer_jeu = 0

				#Touches de déplacement de Donkey Kong
				elif event.key == K_RIGHT:
					if (pc.x,pc.y) not in listepos:
						listepos.append((pc.x,pc.y))
					pc.deplacer('droite')
					ghost.deplacerghost()
				elif event.key == K_LEFT:
					if (pc.x,pc.y) not in listepos:
						listepos.append((pc.x,pc.y))
					pc.deplacer('gauche')
					ghost.deplacerghost()
				elif event.key == K_UP:
					if (pc.x,pc.y) not in listepos:
						listepos.append((pc.x,pc.y))
					pc.deplacer('haut')
					ghost.deplacerghost()
				elif event.key == K_DOWN:
					if (pc.x,pc.y) not in listepos:
						listepos.append((pc.x,pc.y))
					pc.deplacer('bas')
					ghost.deplacerghost()
				elif len(listepos)==nbdogs :
					continuer_jeu = 0
		#Affichages aux nouvelles positions
		fenetre.blit(fond, (0,0))
		niveau.afficher(fenetre)
		niveau.manger(fenetre,listepos)
		fenetre.blit(pc.direction, (pc.x, pc.y)) #dk.direction = l'image dans la bonne direction
		fenetre.blit(ghost.direction, (ghost.x, ghost.y))
		pygame.display.update()

		#Victoire -> Retour à l'accueil
		if niveau.structure[pc.case_y][pc.case_x] == 'a':
			continuer_jeu = 0
