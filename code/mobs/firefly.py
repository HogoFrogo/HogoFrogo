import pygame 
from .enemy import Enemy
from random import randint

class Firefly(Enemy):
	images_folder = 'firefly'
	attack_damage = 0
	healing_points = 3
	minimum_speed = 4
	maximum_speed = 7
	speed_y = 0
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
