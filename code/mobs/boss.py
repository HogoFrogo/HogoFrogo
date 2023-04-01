#region Imports
from math import atan, degrees
import pygame
from mobs.poop import Poop 
from mobs.green_poop import GreenPoop 
from tiles import Tile, AnimatedTile, StaticTile
from random import randint
from player import Player
#endregion

class Boss(AnimatedTile):
	images_folder = ''
	attack_damage = 60
	healing_points = 6
	minimum_speed = 4
	maximum_speed = 12
	boss_type = 'none'
	time_to_shoot_max=60
	time_to_shoot=0
	time_to_shoot_2=0
	health = 4
	def __init__(self,x,y,boss_type):
		size=50
		x=200
		y=200
		self.image = '../graphics/mobs/bosses/flyking/run'
		super().__init__(size,x,y,self.image)

		self.boss_type = boss_type
		self.images_folder=boss_type
		self.time_to_shoot=randint(0,self.time_to_shoot_max)
		self.shoot_sound = pygame.mixer.Sound('../audio/effects/hit.wav')


	#def trigger_action(self,level: Level):
	#	print('Bububu!')
	#	if self.boss_type == 'flyking':
	#		self.shoot(level.player)
	
	def shoot(self,tile,tile_size,color ='brown'):
		distancex = (tile.rect.centerx-self.rect.centerx)
		distancey = (tile.rect.centery-self.rect.centery)
		abs_distancex = abs(distancex)
		abs_distancey = abs(distancey)
		print(abs_distancex+abs_distancey)
		print(self.time_to_shoot)
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
			if color=='brown':
				bullet = Poop(tile_size,self.rect.centerx,self.rect.centery-64,angle,12)
			else:
				bullet = GreenPoop(tile_size,self.rect.centerx,self.rect.centery-64,angle,12)
			return bullet
		if self.time_to_shoot>0:
			self.time_to_shoot-=1
