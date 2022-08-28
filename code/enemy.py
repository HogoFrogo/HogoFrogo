import pygame 
from tiles import AnimatedTile
from random import randint
import math

class Enemy(AnimatedTile):
	image = ""
	def __init__(self,size,x,y):
		super().__init__(size,x,y,self.image)

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