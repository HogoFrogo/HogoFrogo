import pygame 
from .enemy import Enemy
from random import randint

class Wasp(Enemy):
	images_folder = 'wasp'
	attack_damage = 60
	healing_points = 6
	minimum_speed = 4
	maximum_speed = 12
	def __init__(self,size,x,y):
		super().__init__(size,x,y)