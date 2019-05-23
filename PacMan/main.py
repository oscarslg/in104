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
#coeur symbole de vie 
coeur = pygame.image.load(coeur).convert_alpha()
coeur = pygame.transform.scale(coeur,[20,20])

#bandeau vie 
bandeau = pygame.image.load(life).convert_alpha()
bandeau = pygame.transform.scale(bandeau ,[250,27])
#Titre
pygame.display.set_caption(titre_fenetre)

pygame.key.set_repeat(500, 30) #permet de rendre le déplacement continu (delay,interval)
#BOUCLE PRINCIPALE
continuer = 1
while continuer:
	

	#On remet ces variables à 1 à chaque tour de boucle
	continuer_jeu = 1
	continuer_accueil = 1
	vict = 0
	nblife = 3 


	#BOUCLE D'ACCUEIL
	while continuer_accueil and not vict :

		#Chargement et affichage de l'écran d'accueil
		accueil = pygame.image.load(image_accueil).convert()
		accueil = pygame.transform.scale(accueil,[cote_fenetre, cote_fenetre]).convert_alpha()
		fenetre.blit(accueil, (0,0))

		#Rafraichissement
		pygame.display.flip()


		#Limitation de vitesse de la boucle
		#pygame.time.Clock().tick(20)
		for event in pygame.event.get():

			#mettre de la musique 
			# pygame.mixer.music.load("pacman_beginning.wav")
			# pygame.mixer.music.play()

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
				elif event.key == K_c:
					continuer_accueil = 0
					choix = 'n3'


	#on vérifie que le joueur a bien fait un choix de niveau
	#pour ne pas charger s'il quitte
	if choix != 0:
		#Chargement du fond
		fenetre.fill(Color("black"))
		pygame.display.flip()


		#Génération d'un niveau à partir d'un fichier
		niveau = Niveau(choix)
		niveau.generer()
		niveau.afficher(fenetre)


		#Création de pac man
		pc = Perso(droite1, gauche1,haut1,bas1, niveau)
		ghost1 = ghostlevel1(niveau)
		ghost2 = Autobot(niveau)
		listepos=[] #liste des positions par lesquelles est passé pac man 

	#mettre de la musique 
	# pygame.mixer.music.queue("pacman_chomp.wav")
	# pygame.mixer.music.play()
	#BOUCLE DE JEU
	while continuer_jeu and not vict and nblife!=0 :

		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(300)

		for event in pygame.event.get():

			#Si l'utilisateur quitte, on met la variable qui continue le jeu
			#ET la variable générale à 0 pour fermer la fenêtre
			if event.type == QUIT:
				continuer_jeu = 0
				continuer = 0

			elif event.type == KEYDOWN:
					
				numerodirection = random.randint(0,3)
				ghost1.direction = ['haut','bas','droite','gauche'][numerodirection]
				#Si l'utilisateur presse Echap ici, on revient seulement au menu
				if event.key == K_ESCAPE:
					continuer_jeu = 0

				#Touches de déplacement de Pac Man
				elif event.key == K_RIGHT:
					if niveau.structure[pc.case_y][pc.case_x+1] != 'm':
						pc.consigne = 'droite'
														
				elif event.key == K_LEFT:
					if niveau.structure[pc.case_y][pc.case_x-1] != 'm':
						pc.consigne = 'gauche'
						
				elif event.key == K_UP:
					if niveau.structure[pc.case_y-1][pc.case_x] != 'm':
						pc.consigne = 'haut'

				elif event.key == K_DOWN:
					if niveau.structure[pc.case_y+1][pc.case_x] != 'm':
						pc.consigne = 'bas'
					

		if (pc.x,pc.y) not in listepos:
			listepos.append((pc.x,pc.y))
		#déplacement pacman 	
		pc.deplacer(pc.consigne)
		#on vérifie si on est sur un sushi 
		if (pc.case_x,pc.case_y)==(1,18) or (pc.case_x,pc.case_y)==(18,18) or (pc.case_x,pc.case_y)==(1,1) or (pc.case_x,pc.case_y)==(18,1):
			pc.mode='agressif'


		#déplacement du ghost1 en évitant des retour arrière trop fréquent
		ghost1.autodeplacer(ghost1.direction)
		
		#déplacement du ghost1 en évitant des retour arrière trop fréquent
		ghost2.automove()
		
		#dans le cas d'une rencontre en mode vulnérable c'est le pacman qui revient au centre 
		if pc.mode=='vulnerable':
			if (pc.x,pc.y)==(ghost1.x,ghost1.y) or pc.previous==(ghost1.x,ghost1.y) or (pc.x,pc.y)==ghost1.previous:
						nblife-=1
						pc.bump()
			if (pc.x,pc.y)==(ghost2.x,ghost2.y) or pc.previous==(ghost2.x,ghost2.y) or (pc.x,pc.y)==ghost2.previous:
						nblife-=1
						pc.bump()
		#dans le cas aggressif c'est les fantomes qui vont au centre
		else: 
			if (pc.x,pc.y)==(ghost1.x,ghost1.y) or pc.previous==(ghost1.x,ghost1.y) or (pc.x,pc.y)==ghost1.previous:
						ghost1.bump()
						#nblife+=1 on pourrait rajouter ca comme regle : +1 vie quand on croise un fantome 
			if (pc.x,pc.y)==(ghost2.x,ghost2.y) or pc.previous==(ghost2.x,ghost2.y) or (pc.x,pc.y)==ghost2.previous:
						ghost2.bump()
						#nblide+=1 
		if len(listepos)==(niveau.nbdogs+4):
			vict = 1
			
		else :
			#Affichages aux nouvelles positions
			fenetre.fill(Color("black"))
			niveau.afficher(fenetre)
			niveau.manger(fenetre,listepos)
			if pc.mode == 'vulnerable':
				fenetre.blit(pc.direction, (pc.x, pc.y)) 
			else:
				sonicimg = pygame.image.load(sonic).convert()
				sonicimg = pygame.transform.scale(sonicimg,[30,30])
				fenetre.blit(sonicimg,(pc.x,pc.y))
			fenetre.blit(ghost1.tete, (ghost1.x, ghost1.y))
			fenetre.blit(ghost2.tete, (ghost2.x, ghost2.y))
			myfont = pygame.font.SysFont("monospace", 40)
			score_display = myfont.render("score:" + str(len(listepos)), 1, (0,0,0))
			fenetre.blit(score_display, (400, 3))
			if nblife == 1:
				fenetre.blit(bandeau,(0,0))
				fenetre.blit(coeur,(185,3))
			elif nblife == 2:
				fenetre.blit(bandeau,(0,0))
				fenetre.blit(coeur,(155,3))
				fenetre.blit(coeur,(185,3))
			elif nblife == 3:
				fenetre.blit(bandeau,(0,0))
				fenetre.blit(coeur,(155,3))
				fenetre.blit(coeur,(185,3))
				fenetre.blit(coeur,(215,3))

			pygame.display.update()

	#cas où le pacman a utilisé ses 3 vies 
	while nblife==0:
		font = pygame.font.SysFont(None, 72)
		text = font.render('looser!', 1, (255, 255, 255))
		text2 = font.render('score:'+str(len(listepos)), 1, (0, 128, 0))
		fenetre.fill(Color("black"))
		fenetre.blit(text,(170,250))
		fenetre.blit(text2,(190,320))
		pygame.display.update()	
		#mettre de la musique 
		pygame.mixer.music.load("pacman_death.wav")
		pygame.mixer.music.play()	
		for event in pygame.event.get(): 
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				nblife = 1 


	#en cas de victoire 
	while vict : #affichage de l'image de victoire tant que l'on n'appuie pas sur un bouton 
		font = pygame.font.SysFont(None, 72)
		text = font.render('You Win !', 1, (0, 128, 0))
		text2 = font.render('Congratulations !', 1, (0, 128, 0))
		fenetre.fill(Color("black"))
		fenetre.blit(text,(160,250))
		fenetre.blit(text2,(90,320))
		pygame.display.update()		
		for event in pygame.event.get(): 
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				vict = 0 
