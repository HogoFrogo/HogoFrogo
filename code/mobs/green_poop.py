#region Imports
import pygame 
from .poop import Poop
from random import randint
#endregion

class GreenPoop(Poop):
	images_folder = 'green_poop'
	def __init__(self,size,x,y,angle=180,speed = 0):
		super().__init__(size,x,y,angle,speed)