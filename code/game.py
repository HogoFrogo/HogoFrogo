from mimetypes import init
import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI
from game_data import levels


class Game:
	def __init__(self, screen, music_volume):
		# game attributes
		self.max_level = 2
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		self.screen = screen
		programIcon = pygame.image.load('../graphics/character/idle/1.png')
		pygame.display.set_icon(programIcon)
		self.music_volume = music_volume
		
		# audio 
		
		self.level_bg_music = pygame.mixer.Sound('../audio/magnetic_b-ing.mp3')
		self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_croak_music.mp3')


		# overworld creation
		self.difficulty = "Easy"
		self.overworld = Overworld(0,self.max_level,screen,self.create_level,self.difficulty)
		self.status = 'overworld'

		# user interface 
		self.ui = UI(screen)


	def create_level(self,current_level,difficulty):
		self.level = Level(current_level,self.screen,self.create_overworld,self.change_coins,self.change_health,difficulty)
		self.status = 'level'
		self.overworld_bg_music.stop()
		self.level_bg_music = pygame.mixer.Sound(levels[current_level]['level_bg_music'])
		self.level_bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level,difficulty):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,self.screen,self.create_level,difficulty)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)
		self.level_bg_music.stop()

	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount
		if(self.cur_health>self.max_health):
			self.cur_health = self.max_health

	def change_music_volume(self,new_music_volume):
		self.music_volume = new_music_volume
		self.level_bg_music.set_volume(new_music_volume)
		self.overworld_bg_music.set_volume(new_music_volume)

	def check_game_over(self):
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = self.coins-30
			self.overworld = Overworld(0,self.max_level,self.screen,self.create_level,self.difficulty)
			self.status = 'overworld'
			self.level_bg_music.stop()
			self.overworld_bg_music.play(loops = -1)

	def run(self,player_name,difficulty,music_volume):
		if self.status == 'overworld':
			self.overworld.run()
			self.overworld.difficulty =difficulty
		else:
			self.level.run()
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()