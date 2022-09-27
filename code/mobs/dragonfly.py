import pygame 
from .enemy import Enemy
from random import randint

class Dragonfly(Enemy):
	images_folder = 'dragonfly'
	attack_damage = 5
	healing_points = 7
	minimum_speed = 7
	maximum_speed = 10
	speed_y = 5
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
