#region Imports
import pygame 
from .enemy import Enemy
from random import randint
#endregion

class Bullet(Enemy):
	images_folder = 'bullet'
	attack_damage = 8
	healing_points = -1
	minimum_speed = 2
	maximum_speed = 9
	def __init__(self,size,x,y,angle=180,speed = 0):
		super().__init__(size,x,y,speed)
		self.total_speed = self.speed
		self.set_direction(angle)