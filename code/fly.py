import pygame 
from enemy import Enemy
from random import randint

class Fly(Enemy):
	image = '../graphics/fly/run'
	attack_damage = 2
	healing_points = 3
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
		self.speed = -randint(2,9)
		self.rect.y += size - self.image.get_size()[1]