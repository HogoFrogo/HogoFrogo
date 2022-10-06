import pygame

from mobs.bullet import Bullet 
from .enemy import Enemy
from random import randint

class GangsterFrog(Enemy):
	images_folder = 'gangster_frog'
	attack_damage = 7
	healing_points = 4
	minimum_speed = 2
	maximum_speed = 5
	time_to_shoot_max=60
	time_to_shoot=0
	
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
		self.time_to_shoot=0

	def shoot(self,tile,tile_size):
		if(self.time_to_shoot==0):
			print("bang!")
			# get coordinates of the other tile
			# set dirwection of bullet by the coordinates
			# self.time_to_shoot = 60
			bullet = Bullet(tile_size,self.rect.x,self.rect.y,randint(0,359),12)
			return bullet
