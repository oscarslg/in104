"""Classes du jeu Pacman"""

import pygame
from pygame.locals import * 
from constantes import *

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
		mur = pygame.image.load("mur.png").convert()
		mur = pygame.transform.scale(mur,[30,30])
		depart = pygame.image.load(image_depart).convert()
		arrivee = pygame.image.load(image_arrivee).convert_alpha()
		hotdog = pygame.image.load(image_nourriture).convert_alpha()
		hotdog = pygame.transform.scale(hotdog,[20,20])

		#On parcourt la liste du niveau
		num_ligne = 0
		nbdogs=0 #compteur des dogs afin de savoir quand l'utilisateur a tout mangé 
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
				elif sprite == 'a':		   #a = Arrivée
					fenetre.blit(arrivee, (x,y))
				else :
					fenetre.blit(hotdog,(x+5,y+5))
					nbdogs+=1
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
	def __init__(self, droite, gauche, haut, bas, niveau,mou):
		#Sprites du personnage
		self.droite = pygame.image.load("droite.png").convert_alpha()
		self.droite = pygame.transform.scale(self.droite,[30,30])
		self.gauche = pygame.image.load("gauche.png").convert_alpha()
		self.gauche = pygame.transform.scale(self.gauche,[30,30])
		self.haut = pygame.image.load("haut.png").convert_alpha()
		self.haut = pygame.transform.scale(self.haut,[30,30])
		self.bas = pygame.image.load("bas.png").convert_alpha()
		self.bas = pygame.transform.scale(self.bas,[30,30])
		#Position du personnage en cases et en pixels
		self.case_x = 1
		self.case_y = 1
		self.x = 30
		self.y = 30
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau
		self.chasse= mou
	
	def chasseur(self,listesushi):
		for couple in listepos:
			if couple in listesushi:
				self.chasse=agressif
				listesushi.remove(couple)
			time.sleep(7.0)
			self.chasse=mou
	
	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""
		
		#Déplacement vers la droite
		if direction == 'droite':
			#Pour ne pas dépasser l'écran
			if self.case_x < (nombre_sprite_cote - 1):
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
			if self.case_x > 0:
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
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * taille_sprite
			self.direction = self.bas
		
	def mangerfantome(self, agressif, Ghost):
		if self.chasse=agressif:
			for couple in listepos:
				if couple==(Ghost.x,Ghost.y):
					Ghost.x=10
					Ghost.y=10
			
	
class Ghost:
     def __init__(self, droite, gauche, haut, bas, niveau):
        #Sprites du personnage
        self.droite = pygame.image.load(droite)
        self.droite = pygame.transform.scale(self.droite,[30,30]).convert_alpha()
        self.gauche = pygame.image.load(gauche)
        self.gauche = pygame.transform.scale(self.gauche,[30,30]).convert_alpha()
        self.haut = pygame.image.load(haut)
        self.haut = pygame.transform.scale(self.haut,[30,30]).convert_alpha()
        self.bas = pygame.image.load(bas)
        self.bas = pygame.transform.scale(self.bas,[30,30]).convert_alpha()
        #Position du personnage en cases et en pixels
        self.case_x = 10
        self.case_y = 10
        self.x = self.case_x * taille_sprite
        self.y = self.case_y * taille_sprite
        #Direction par défaut
        self.direction = self.droite
        #Niveau dans lequel le personnage se trouve 
        self.niveau = niveau
        
     def deplacer(self, direction):
        """Methode permettant de déplacer le personnage"""
        
        #Déplacement vers la droite
        if direction == 'droite':
            #Pour ne pas dépasser l'écran
            if self.case_x < (nombre_sprite_cote - 1):
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
            if self.case_x > 0:
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
                if self.niveau.structure[self.case_y+1][self.case_x] != 'm':
                    self.case_y += 1
                    self.y = self.case_y * taille_sprite
            self.direction = self.bas
