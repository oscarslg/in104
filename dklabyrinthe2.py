#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Jeu Donkey Kong Labyrinthe
Jeu dans lequel on doit déplacer DK jusqu'aux bananes à travers un labyrinthe.

Script Python
Fichiers : dklabyrinthe.py, classes.py, constantes.py, n1, n2 + images
"""

#dans cette version, on cherche ne pas modifier le script de classe mais on veut que le bonhomme ne s'arrpete pas en rencontrant un mur


import pygame
from pygame.locals import *

from classes import *
from constantes import *

pygame.init()

#Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))
#Icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption(titre_fenetre)


#BOUCLE PRINCIPALE
continuer = 1
while continuer:
	#Chargement et affichage de l'écran d'accueil
	accueil = pygame.image.load(image_accueil).convert()
	fenetre.blit(accueil, (0,0))

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

		#Génération d'un niveau à partir d'un fichier
		niveau = Niveau(choix)
		niveau.generer()
		niveau.afficher(fenetre)

		#Création de Donkey Kong
		dk = Perso("dk_droite.png", "dk_gauche.png",
		"dk_haut.png", "dk_bas.png", niveau)


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
					i=1
					while event.key != KEYDOWN and i<nombre_sprite_cote : #on fixe imax a nombre_sprite_cote  = nb deplacement maxi 
						pygame.time.delay(30)
						dk.deplacer('droite')
						i+=1
						#Affichages aux nouvelles positions
						fenetre.blit(fond, (0,0))
						niveau.afficher(fenetre)
						fenetre.blit(dk.direction, (dk.x, dk.y)) #dk.direction = l'image dans la bonne direction
						pygame.display.flip()
				elif event.key == K_LEFT:
					i=1
					while event.key != KEYDOWN and i<nombre_sprite_cote :
						pygame.time.delay(30)
						dk.deplacer('gauche')
						i+=1
						#Affichages aux nouvelles positions
						fenetre.blit(fond, (0,0))
						niveau.afficher(fenetre)
						fenetre.blit(dk.direction, (dk.x, dk.y)) #dk.direction = l'image dans la bonne direction
						pygame.display.flip()
				elif event.key == K_UP:
					i=1
					while event.key != KEYDOWN and i<nombre_sprite_cote :
						pygame.time.delay(30)
						dk.deplacer('haut')
						i+=1
						#Affichages aux nouvelles positions
						fenetre.blit(fond, (0,0))
						niveau.afficher(fenetre)
						fenetre.blit(dk.direction, (dk.x, dk.y)) #dk.direction = l'image dans la bonne direction
						pygame.display.flip()
				elif event.key == K_DOWN:
					i=1
					while event.key != KEYDOWN and i<nombre_sprite_cote :
						pygame.time.delay(30)
						dk.deplacer('bas')
						i+=1
						#Affichages aux nouvelles positions
						fenetre.blit(fond, (0,0))
						niveau.afficher(fenetre)
						fenetre.blit(dk.direction, (dk.x, dk.y)) #dk.direction = l'image dans la bonne direction
						pygame.display.flip()

		#Affichages aux nouvelles positions
		fenetre.blit(fond, (0,0))
		niveau.afficher(fenetre)
		fenetre.blit(dk.direction, (dk.x, dk.y)) #dk.direction = l'image dans la bonne direction
		pygame.display.flip()

		#Victoire -> Retour à l'accueil
		if niveau.structure[dk.case_y][dk.case_x] == 'a':
			continuer_jeu = 0
