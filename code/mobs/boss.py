import pygame 
from tiles import Tile, StaticTile
from .enemy import Enemy
from random import randint
from player import Player

class Boss(Enemy):
	images_folder = ''
	attack_damage = 60
	healing_points = 6
	minimum_speed = 4
	maximum_speed = 12
	boss_type = 'none'
	def __init__(self,boss_type):
		self.boss_type = boss_type
		self.images_folder=boss_type


	#def trigger_action(self,level: Level):
	#	print('Bububu!')
	#	if self.boss_type == 'flyking':
	#		self.shoot(level.player)
	
	def shoot(tile: Tile):
		print('bang!')