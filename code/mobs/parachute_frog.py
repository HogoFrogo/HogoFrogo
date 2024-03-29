#region Imports
import pygame 
from .enemy import Enemy
from random import randint
#endregion

class ParachuteFrog(Enemy):
	images_folder = 'parachute_frog'
	attack_damage = 7
	healing_points = 4
	minimum_speed = 2
	maximum_speed = 9
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
		self.speed = 0
		self.rect.y += size - self.image.get_size()[1]
		self.speed_y = randint(2,9)