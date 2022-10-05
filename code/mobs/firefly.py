import pygame 
from .enemy import Enemy
from random import randint

class Firefly(Enemy):
	images_folder = 'firefly'
	attack_damage = 0
	healing_points = 3
	minimum_speed = 7
	maximum_speed = 10
	speed_y = 5
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
