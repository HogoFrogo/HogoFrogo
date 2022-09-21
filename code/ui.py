import pygame

class UI:
	def __init__(self,surface):

		# setup 
		self.display_surface = surface 

		# health 
		self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
		self.health_bar_topleft = (54,39)
		self.bar_max_width = 152
		self.bar_height = 4

		# jump
		self.jump_bar_y = 84
		self.jump_bar = pygame.image.load('../graphics/ui/jump_bar.png').convert_alpha()
		self.jump_bar_topleft = (54,self.jump_bar_y)
		self.bar_max_width = 152
		self.bar_height = 4
		
		# coins 
		self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
		self.coin_rect = self.coin.get_rect(topleft = (21,115))
		self.font = pygame.font.Font('../graphics/ui/ARCADEPI.ttf',30)

	def show_health(self,current,full):
		self.display_surface.blit(self.health_bar,(20,10))
		current_health_ratio = current / full
		current_bar_width = self.bar_max_width * current_health_ratio
		health_bar_rect = pygame.Rect(self.health_bar_topleft,(current_bar_width,self.bar_height))
		pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

	def show_jump(self,current,full):
		self.display_surface.blit(self.jump_bar,(20,self.jump_bar_y-29))
		current_jump_ratio = current / full
		current_bar_width = self.bar_max_width * current_jump_ratio
		jump_bar_rect = pygame.Rect(self.jump_bar_topleft,(current_bar_width,self.bar_height))
		pygame.draw.rect(self.display_surface,'#7B7CF8',jump_bar_rect)
	
	def show_coins(self,amount):
		self.display_surface.blit(self.coin,self.coin_rect)
		coin_amount_surf = self.font.render(str(amount),False,'#33323d')
		coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
		self.display_surface.blit(coin_amount_surf,coin_amount_rect)