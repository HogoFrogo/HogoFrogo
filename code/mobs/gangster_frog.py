#region Imports
from math import atan, degrees
import pygame
from mobs.bullet import Bullet 
from .enemy import Enemy
from random import randint
#endregion

class GangsterFrog(Enemy):
	images_folder = 'gangster_frog'
	attack_damage = 7
	healing_points = 4
	minimum_speed = 2
	maximum_speed = 5
	time_to_shoot_max=60
	time_to_shoot=0
	time_to_shoot_2=0
	
	def __init__(self,size,x,y):
		super().__init__(size,x,y)
		self.time_to_shoot=randint(0,self.time_to_shoot_max)
		self.shoot_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

	def shoot(self,tile,tile_size):
		distancex = (tile.rect.centerx-self.rect.centerx)
		distancey = (tile.rect.centery-self.rect.centery)
		abs_distancex = abs(distancex)
		abs_distancey = abs(distancey)
		print(abs_distancex+abs_distancey)
		print(self.time_to_shoot)
		if((abs_distancex+abs_distancey)/2<300):
			if(self.time_to_shoot==0):
				print("bang!")
				self.shoot_sound.play()
				# get coordinates of the other tile
				# set dirwection of bullet by the coordinates
				self.time_to_shoot = 30
				## print(tile.rect.center)
				if(abs_distancex==0):
					angle=0
				else:
					gen_angle=degrees(atan(abs_distancey/abs_distancex))
					if distancey>0 and distancex>0:
						angle = gen_angle
					if distancey<=0 and distancex>0:
						angle = 360-gen_angle
					if distancey>0 and distancex<0:
						angle = 180-gen_angle
					if distancey<=0 and distancex<0:
						angle = 180+gen_angle
				#print(distancex)
				#print(distancey)
				#print(angle)
				bullet = Bullet(tile_size,self.rect.centerx,self.rect.centery-64,angle,12)
				return bullet
		if self.time_to_shoot>0:
			self.time_to_shoot-=1
