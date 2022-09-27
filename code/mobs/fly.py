import pygame 
from .enemy import Enemy
from random import randint

class Fly(Enemy):
	images_folder = 'fly'
	attack_damage = 2
	healing_points = 3
	minimum_speed = 2
	maximum_speed = 9
	def __init__(self,size,x,y,angle=180,speed = 0):
		super().__init__(size,x,y)
		if angle != 180:
			self.set_direction(angle)