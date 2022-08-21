import pygame 
from enemy import Enemy
from random import randint

class Ant(Enemy):
	image = '../graphics/ant/run'
	attack_damage = 10
	healing_points = 5
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
		self.speed = randint(2,9)
		self.rect.y += size - self.image.get_size()[1]
		self.speed_y = 0