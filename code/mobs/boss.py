import pygame 
from .enemy import Enemy
from random import randint

class Boss(Enemy):
	images_folder = 'wasp'
	attack_damage = 60
	healing_points = 6
	minimum_speed = 4
	maximum_speed = 12
	boss_type = "none"
	def __init__(self,boss_type):
		self.boss_type = boss_type

	def trigger_action(self,level):
		print("Bububu!")