import pygame 
from enemy import Enemy
from random import randint

class Dragonfly(Enemy):
	image = '../graphics/dragonfly/run'
	attack_damage = 5
	healing_points = 6
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
		self.speed = -randint(7,10)
		self.rect.y += size - self.image.get_size()[1]
        