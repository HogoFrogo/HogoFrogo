#region Imports
import pygame 
from .enemy import Enemy
from random import randint
#endregion
class Ant(Enemy):
	images_folder = 'ant'
	attack_damage = 10
	healing_points = 5
	minimum_speed = 2
	maximum_speed = 9
	def __init__(self,size,x,y):
		super().__init__(size,x,y)