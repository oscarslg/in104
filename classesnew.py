def afficher(self, fenetre):
		"""Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()"""
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		mur = pygame.image.load("mur.png").convert()
		mur = pygame.transform.scale(mur,[30,30])
		depart = pygame.image.load(image_depart).convert()
		arrivee = pygame.image.load(image_arrivee).convert_alpha()
		hotdog = pygame.image.load(image_nourriture).convert_alpha()
		sushi = pygame.image.load(image_attaque).convert_alpha()
		fantome = pygame.image.load(image_ghost).convert_alpha()
		noir= pygame.image.load(black).convert_alpha()
		self.hotdog = pygame.transform.scale(hotdog,[20,20])

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
					fenetre.blit(sushi, (x,y))				
				elif sprite == 'b':		   #b=black
					fenetre.blit(noir, (x,y))				
				else :
					fenetre.blit(self.hotdog,(x+5,y+5))
					self.nbdogs+=1
				num_case += 1
			num_ligne += 1
	
