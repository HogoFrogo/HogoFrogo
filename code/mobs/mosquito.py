#region Imports
import pygame 
from .enemy import Enemy
from random import randint
#endregion

class Mosquito(Enemy):
	images_folder = 'mosquito'
	attack_damage = 7
	healing_points = 2
	minimum_speed = 2
	maximum_speed = 9
	def __init__(self,size,x,y,angle=180,speed = 0):
		super().__init__(size,x,y)
		if angle != 180:
			self.set_direction(angle)