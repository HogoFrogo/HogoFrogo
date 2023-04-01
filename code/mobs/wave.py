#region Imports
import pygame 
from .enemy import Enemy
from random import randint
#endregion

class Wave(Enemy):
	images_folder = 'wave'
	attack_damage = 100
	healing_points = 3
	minimum_speed = 3
	maximum_speed = 5
	def __init__(self,size,x,y,angle=0,speed = 0):
		super().__init__(size,x,y)
		self.total_speed = speed
		self.set_direction(angle)