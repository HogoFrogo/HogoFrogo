#region Imports
import pygame 
from .enemy import Enemy
from random import randint
#endregion

class Poop(Enemy):
	images_folder = 'poop'
	attack_damage = 8
	healing_points = -10
	minimum_speed = 2
	maximum_speed = 9
	def __init__(self,size,x,y,angle=180,speed = 0):
		super().__init__(size,x,y,speed)
		self.total_speed = self.speed
		if angle != 180:
			self.set_direction(angle)