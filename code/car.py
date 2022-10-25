import pygame 
from tiles import AnimatedTile
from random import randint
import math

class Car(AnimatedTile):
	image = ""
	images_folder = ""
	attack_damage = 0
	healing_points = 0
	speed_x = 0
	speed_y = 0
	minimum_speed = 0
	maximum_speed = 0
	def __init__(self,size,x,y,speed_x=0,speed_y=0):
		self.image = '../graphics/cars/1/run'
		self.initialize_speed()
		if speed_x==0:
			self.speed = self.speed_x
		else:
			self.speed = speed_x
		if speed_y!=0:
			self.speed_y = speed_y
		super().__init__(size,x,y,self.image)
		self.rect.y += size - self.image.get_size()[1]

	def move(self):
		self.rect.x += self.speed
		self.rect.y += self.speed_y

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()

	def set_direction(self, angle):
		self.speed_y = math.sin(math.radians(angle))*self.total_speed
		self.speed = math.cos(math.radians(angle))*self.total_speed

	def initialize_speed(self):
		self.speed_x = 2