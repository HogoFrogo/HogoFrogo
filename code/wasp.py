import pygame 
from enemy import Enemy
from random import randint

class Wasp(Enemy):
	image = '../graphics/wasp/run'
	attack_damage = 60
	healing_points = 4
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
		self.speed = -randint(4,12)
		self.rect.y += size - self.image.get_size()[1]
		self.speed_y = 0