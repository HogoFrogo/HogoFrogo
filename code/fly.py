import pygame 
from enemy import Enemy
from random import randint

class Fly(Enemy):
	image = '../graphics/fly/run'
	attack_damage = 2
	healing_points = 3
	def __init__(self,size,x,y,angle=180,speed = 0):
		super().__init__(size,x,y)
		if speed ==0:
			self.total_speed = randint(2,9)
		else:
			self.total_speed = speed
		self.speed = -self.total_speed
		self.rect.y += size - self.image.get_size()[1]
		self.speed_y = 0
		if angle != 180:
			self.set_direction(angle)