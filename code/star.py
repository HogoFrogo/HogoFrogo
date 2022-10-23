import pygame
from tiles import StaticTile


class Star(StaticTile):
	def __init__(self,size,x,y):
		image = pygame.image.load('../graphics/star.png')
		
		image_scaled = pygame.transform.scale(image, (15, 15))

		super().__init__(size,x,y,image_scaled.convert_alpha())
		offset_y = y + size
		self.rect = image_scaled.get_rect(bottomleft = (x,offset_y))

# vyřešit zakrývání hvězd mraky, palmami, hmyzáky atd.
# bylo by dobré, aby svítily 