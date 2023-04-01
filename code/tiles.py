#region Imports
import pygame 
from support import import_folder
#endregion

class Tile(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,shift):
		self.rect.x += shift

class StaticTile(Tile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface 

class Terrain(StaticTile):
	stable=True
	fall_speed = 10
	time_before_fall = 60
	def __init__(self,size,x,y,surface,position=0,stable=True):
		super().__init__(size,x,y,surface)
		self.position=position
		self.stable=stable
		self.state="static"
		
	def update(self,shift):
		super().update(shift)
		if self.state=="to_be_falling":
			self.time_before_fall -=1
			if self.time_before_fall<1:
				self.state="falling"

		if(not self.stable and self.state=="falling"):
			self.rect.y += self.fall_speed

class Crate(StaticTile):
	def __init__(self,size,x,y,biome):
		super().__init__(size,x,y,pygame.image.load('../graphics/bioms/'+biome+'/terrain/crate.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Stone(StaticTile):
	def __init__(self,size,x,y,biome):
		super().__init__(size,x,y,pygame.image.load('../graphics/stone.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTile(Tile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,shift):
		self.animate()
		self.rect.x += shift

class Coin(AnimatedTile):
	def __init__(self,size,x,y,path,value):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = value

class Palm(AnimatedTile):
	def __init__(self,size,x,y,path,offset):
		super().__init__(size,x,y,path)
		offset_y = y - offset
		self.rect.topleft = (x,offset_y)

class House(AnimatedTile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y,path)
		offset_y = y - 72
		self.rect.topleft = (x,offset_y)
		#offset_y = y + size
		#self.rect = self.image.get_rect(bottomleft = (x,offset_y))
		
class Constraint(StaticTile):
	def __init__(self,size,x,y,value,biome):
		super().__init__(size,x,y,pygame.image.load('../graphics/bioms/'+biome+'/terrain/crate.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))
		self.value = value