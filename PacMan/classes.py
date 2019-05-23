"""Classes du jeu Pacman"""

import pygame
from pygame.locals import * 
from constantes import *
import random 
class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0
	
	
	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""	
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau
	
	
	def afficher(self, fenetre):
		"""Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()"""
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		mur = pygame.image.load(mur1).convert()
		mur = pygame.transform.scale(mur,[30,30])
		hotdog = pygame.image.load(image_nourriture).convert_alpha()
		self.hotdog = pygame.transform.scale(hotdog,[20,20])
		sushi = pygame.image.load(sushi1).convert_alpha()
		self.sushi = pygame.transform.scale(sushi,[20,20])
		noir= pygame.image.load(black).convert_alpha()

		#On parcourt la liste du niveau
		num_ligne = 0
		self.nbdogs=0 #compteur des dogs afin de savoir quand l'utilisateur a tout mangé 
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'm':		   #m = Mur
					fenetre.blit(mur, (x,y))
				elif sprite == 'd':		   #d = Départ
					fenetre.blit(depart, (x,y))
				elif sprite == 'g':		   #g = ghost
					fenetre.blit(fantome, (x,y))
				elif sprite == 's':		   #s = sushi
					fenetre.blit(self.sushi, (x+5,y+5))				
				elif sprite == 'b':		   #b=black
					fenetre.blit(noir, (x,y))				
				else :
					fenetre.blit(self.hotdog,(x+5,y+5))
					self.nbdogs+=1
				num_case += 1
			num_ligne += 1

		 
	
	def manger(self,fenetre,listepos): 
		""" Méthode permettant d'afficher des carrés noir a la place des 
		dogs une fois ces derniers mangés """
		carrenoir = pygame.image.load(black).convert()
		carrenoir = pygame.transform.scale(carrenoir,[30,30])
		for couple in listepos:
			fenetre.blit(carrenoir,couple)
		
			
			
class Perso:
	"""Classe permettant de créer un personnage"""
	def __init__(self, droite, gauche, haut, bas, niveau):
		#Sprites du personnage
		self.droite = pygame.image.load(droite1).convert_alpha()
		self.droite = pygame.transform.scale(self.droite,[30,30])
		self.gauche = pygame.image.load(gauche1).convert_alpha()
		self.gauche = pygame.transform.scale(self.gauche,[30,30])
		self.haut = pygame.image.load(haut1).convert_alpha()
		self.haut = pygame.transform.scale(self.haut,[30,30])
		self.bas = pygame.image.load(bas1).convert_alpha()
		self.bas = pygame.transform.scale(self.bas,[30,30])
		#Position du personnage en cases et en pixels
		self.case_x = 7
		self.case_y = 10 #le pac man commence en dehors du terrier au début de la partie 
		self.x = 30*self.case_x
		self.y = 30*self.case_y
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau
		self.consigne=''
		self.previous=(0,0)
		self.mode = 'vulnerable' #en temps normal le pac man est vulnérable 
	
	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""
		self.previous=(self.x,self.y)
		#Déplacement vers la droite
		if direction == 'droite':
			
			if self.case_x == nombre_sprite_cote-1 and self.case_y == ytunnel :
				self.case_x = 0
				self.x = self.case_x * taille_sprite

			#Pour ne pas dépasser l'écran
			elif self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
			#Image dans la bonne direction
			self.direction = self.droite
		
		#Déplacement vers la gauche
		if direction == 'gauche':
			if self.case_x == 0 and self.case_y == ytunnel :
				self.case_x = nombre_sprite_cote
				self.x = self.case_x * taille_sprite
			elif self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
			self.direction = self.gauche
		
		#Déplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
			self.direction = self.haut
		
		#Déplacement vers le bas
		if direction == 'bas':
			if self.case_y < (nombre_sprite_cote - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm' :
					if (self.case_x,self.case_y)!= (xprison,yprison) and (self.case_x,self.case_y)!= (xprison+1,yprison) :
						#on a ajouter une condition pour ne pas pouvoir rerentrer dans la prison 
						self.case_y += 1
						self.y = self.case_y * taille_sprite
			self.direction = self.bas

	def bump (self): #permet de remettre le pac man au centre du terrain après avoir été mangé 
		self.case_x = 7
		self.case_y = 8
		self.x = 30*self.case_x
		self.y = 30*self.case_y
		self.consigne='' #le pacman sort de son terrier directement 




class ghostlevel1:
	"""Classe permettant de créer un personnage"""
	def __init__(self,niveau):
		#Sprites du personnage
		self.tete = pygame.image.load(ghost1).convert_alpha()
		self.tete = pygame.transform.scale(self.tete,[30,30])
		
		#Position du personnage en cases et en pixels
		self.case_x = 7
		self.case_y = 8 #le ghost commence dans le  terrier au début de partie 
		self.x = 30*self.case_x
		self.y = 30*self.case_y
		#Direction par défaut
		self.niveau = niveau
		self.direction = 'haut'
		self.previous=(0,0)
	
	
	def autodeplacer(self,direction):
		"""Methode permettant de déplacer le personnage"""
		
		self.previous=(self.x,self.y)
		#Déplacement vers la droite
		if direction == 'droite':
			
			if self.case_x == nombre_sprite_cote-1 and self.case_y == ytunnel :
				self.case_x = 0
				self.x = self.case_x * taille_sprite

			#Pour ne pas dépasser l'écran
			elif self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
			
		
		#Déplacement vers la gauche
		if direction == 'gauche':
			if self.case_x == 0 and self.case_y == ytunnel :
				self.case_x = nombre_sprite_cote
				self.x = self.case_x * taille_sprite
			elif self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
			
		
		#Déplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
			
		
		#Déplacement vers le bas
		if direction == 'bas':
			if self.case_y < (nombre_sprite_cote - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm' :
					if (self.case_x,self.case_y)!= (xprison,yprison) and (self.case_x,self.case_y)!= (xprison+1,yprison) :
						#on a ajouter une condition pour ne pas pouvoir rerentrer dans la prison 
						self.case_y += 1
						self.y = self.case_y * taille_sprite

	def bump (self): #permet de remettre le fantome au centre du terrain après avoir été mangé 
		self.case_x = 7
		self.case_y = 8
		self.x = 30*self.case_x
		self.y = 30*self.case_y
		self.direction = 'haut' 


class Autobot:
	def __init__(self, niveau):
		#Sprites du personnage
		self.tete = pygame.image.load(ghost2)
		self.tete = pygame.transform.scale(self.tete,[30,30]).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 8
		self.case_y = 7
		self.x = self.case_x * taille_sprite
		self.y = self.case_y * taille_sprite
		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau
		#debut de la direction privilégié
		self.direction = 0
		self.previous=(0,0)
		
	def automove(self):
		self.previous=(self.x,self.y)
		#deplacement haut direct
		if self.direction == 0:
			if self.niveau.structure[self.case_y-1][self.case_x] != 'm'  :
				self.case_y -=1
				self.y = self.case_y * taille_sprite
				self.direction = 0
			elif self.niveau.structure[self.case_y][self.case_x-1] != 'm' :
				self.case_x -=1
				self.x = self.case_x * taille_sprite
				self.direction = random.randint(0,3)
			elif self.niveau.structure[self.case_y][self.case_x+1] != 'm' :
				self.case_x +=1
				self.x = self.case_x * taille_sprite
				self.direction = 3
			else:
				self.direction = 2
		elif self.direction == 1:
			if self.niveau.structure[self.case_y][self.case_x-1]!='m' and self.case_x!=0 :
				self.case_x -=1
				self.x=self.case_x * taille_sprite
				self.direction = 1
			elif self.niveau.structure[self.case_y+1][self.case_x] != 'm'  :
				self.case_y +=1
				self.y = self.case_y * taille_sprite
				self.direction = random.randint(0,3)
			elif self.niveau.structure[self.case_y-1][self.case_x] != 'm'  :
				self.case_y -=1
				self.y = self.case_y * taille_sprite
				self.direction = 0
			else:
				self.direction = 3
		elif self.direction == 2:
			if (self.case_x,self.case_y)!= (xprison,yprison) and (self.case_x,self.case_y)!= (xprison+1,yprison) :
						#on a ajouter une condition pour ne pas pouvoir rerentrer dans la prison 
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm'  :
					self.case_y +=1
					self.y = self.case_y * taille_sprite
					self.direction = 2
				elif self.niveau.structure[self.case_y][self.case_x+1] != 'm' :
					self.case_x +=1
					self.x = self.case_x * taille_sprite
					self.direction = random.randint(0,3)
				elif self.niveau.structure[self.case_y][self.case_x-1] != 'm' :
					self.case_x -=1
					self.x = self.case_x * taille_sprite
					self.direction = 1
				else:
					self.direction = 0
		else:
			if self.niveau.structure[self.case_y][self.case_x+1]!='m' and self.case_x!=20:
				self.case_x +=1
				self.x=self.case_x * taille_sprite
				self.direction = 3
			elif self.niveau.structure[self.case_y-1][self.case_x] != 'm'  :
				self.case_y -=1
				self.y = self.case_y * taille_sprite
				self.direction = random.randint(0,3)
			elif self.niveau.structure[self.case_y+1][self.case_x] != 'm'  :
				self.case_y +=1
				self.y = self.case_y * taille_sprite
				self.direction = 2
			else:

				self.direction = 1
	
	def bump (self): #permet de remettre le fantome au centre du terrain après avoir été mangé 
		self.case_x = 7
		self.case_y = 8
		self.x = 30*self.case_x
		self.y = 30*self.case_y
		self.direction = 'haut' 
