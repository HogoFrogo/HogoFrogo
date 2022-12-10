from multiprocessing.connection import wait
from time import sleep
from typing_extensions import Self
import pygame, sys
import pygame_menu
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI
from game import Game

class Program:
	font = pygame_menu.font.FONT_8BIT
	THEME_HOGO_FROGO = pygame_menu.Theme(
		background_color=(40, 121, 35),
		cursor_color=(255, 255, 255),
		cursor_selection_color=(80, 80, 80, 120),
		scrollbar_color=(39, 41, 42),
		scrollbar_slider_color=(65, 66, 67),
		scrollbar_slider_hover_color=(90, 89, 88),
		selection_color=(255, 255, 255),
		title_background_color=(47, 88, 51),
		title_font_color=(215, 215, 215),
		widget_font_color=(200, 200, 200),
		title_font=font,
		widget_font=font,
		widget_font_shadow=True,
		widget_font_shadow_color=(20, 20, 20),
		widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(
		arrow_right_margin=50,
	)
	)
	PROGRAM_NAME = "Hogo Frogo: The Unexpected Adventure"

	def __init__(self):
		# Pygame setup
		pygame.init()
		pygame.display.set_caption(self.PROGRAM_NAME)
		self.screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()

        
        # Load Settings
		self.settings=self.load_settings_from_file()
		self.music_volume = self.settings["music_volume"]
		self.sounds_volume = self.settings["sounds_volume"]
		self.master_volume = self.settings["master_volume"]
		self.main_menu_music_path = '../audio/magnetic_b-ing.mp3'

		self.main_menu_music = pygame.mixer.Sound(self.main_menu_music_path)
		self.main_menu_music.set_volume(self.music_volume)

		self.game = Game(self.screen, self.music_volume, self.sounds_volume, self.master_volume)

		self.play_menu = self.create_play_menu()
		self.credits_menu = self.create_credits_menu()
		self.settings_menu = self.create_settings_menu()

		self.main_menu = self.create_main_menu()

	def run(self):
		self.run_launch_screen()
		self.main_menu_music.play(loops = -1)
		self.main_menu.mainloop(self.screen)

	#settings loading
	def load_settings_from_file(self):
		with open('settings.conf', 'r') as f:
			option = f.readline().split(" = ")
			music_volume = float(option[1])
			option = f.readline().split(" = ")
			sounds_volume = float(option[1])
			option = f.readline().split(" = ")
			master_volume = float(option[1])
		return {"music_volume": music_volume, "sounds_volume": sounds_volume, "master_volume": master_volume}

	#settings saving
	def save_settings_into_file(self):
		with open('settings.conf', 'w') as f:
			f.write("music_volume = " + str(self.game.music_volume) + "\n")
			f.write("sounds_volume = " + str(self.game.sounds_volume) + "\n")
			f.write("master_volume = " + str(self.game.master_volume) + "\n")

	def change_music_volume(self,new_music_volume):
		new_music_volume = new_music_volume/100
		self.game.change_music_volume(new_music_volume)
		self.main_menu_music.set_volume(self.game.music_volume)
		self.save_settings_into_file()

	def change_sounds_volume(self,new_sounds_volume):
		new_sounds_volume = new_sounds_volume/100
		self.game.change_sounds_volume(new_sounds_volume)	
		self.save_settings_into_file()

	def change_master_volume(self, new_sounds_volume):
		new_sounds_volume = new_sounds_volume/100
		self.game.change_master_volume(new_sounds_volume)
		self.save_settings_into_file()

	def toggle_fullscreen(self):
		print('Will toggle fullscreen')

	def create_credits_menu(self):
		credits_menu = pygame_menu.Menu('Credits', screen_width, screen_height,
						theme=self.THEME_HOGO_FROGO)
		credits_menu.add.label("Level Design")
		credits_menu.add.label("Person 1")
		credits_menu.add.label("Boss Design")
		credits_menu.add.label("Person 2")
		credits_menu.add.label("Story")
		credits_menu.add.label("Person 3\nPerson 4\nPerson 5")
		credits_menu.add.label("Programming")
		credits_menu.add.label("Person 6\nPerson 7\nPerson 8")
		credits_menu.add.label("Graphics")
		credits_menu.add.label("Person 9")
		credits_menu.add.label("Music")
		credits_menu.add.label("Person 10")
		credits_menu.add.label("Special Thanks To")
		credits_menu.add.label("Clear Code YT Channel")
		return credits_menu

	def create_settings_menu(self):
		settings_menu = pygame_menu.Menu('Settings', screen_width, screen_height,
							theme=self.THEME_HOGO_FROGO)
		self.volume_slider = settings_menu.add.range_slider('Music Volume', self.music_volume*100, [0, 100], 1, self.change_music_volume)
		self.sounds_volume_slider = settings_menu.add.range_slider('Sounds Volume', self.sounds_volume*100, [0, 100], 1, self.change_sounds_volume)
		self.master_volume_slider = settings_menu.add.range_slider("Master Volume", self.master_volume*100, [0, 100], 1, self.change_master_volume)
		self.full_screen_checkbox = settings_menu.add.button('Fullscreen', self.toggle_fullscreen)
		return settings_menu

	def create_main_menu(self):
		main_menu = pygame_menu.Menu(self.PROGRAM_NAME, screen_width, screen_height,
						theme=self.THEME_HOGO_FROGO)
		main_menu.add.menu_link(self.play_menu, 'Play')
		main_menu.add.button('Play', self.play_menu)
		main_menu.add.menu_link(self.settings_menu, 'Settings')
		main_menu.add.button('Settings', self.settings_menu)
		main_menu.add.menu_link(self.credits_menu, 'Credits')
		main_menu.add.button('Credits', self.credits_menu)
		main_menu.add.button('Quit', pygame_menu.events.EXIT)
		return main_menu

	def create_play_menu(self):
		play_menu = pygame_menu.Menu('Play', screen_width, screen_height,
						theme=self.THEME_HOGO_FROGO)
		#self.name_text_input = play_menu.add.text_input('PlayerName: ', default='Mr. Croak')
		self.difficulty_input = play_menu.add.selector('Difficulty :', [('Toad', 1), ('Frog', 2)])
		play_menu.add.button('Play', self.start_the_game)
		return play_menu

	def run_launch_screen(self):
		print('launch')
		#self.screen.fill('grey')

		window = (700,500)
		background = pygame.Surface(window)

		myimage = pygame.image.load('../graphics/hogo_frogo_teamo_logo.png')
		picture = pygame.transform.scale(myimage, (600, 400))
		
		x1, y1 = background.get_width()//2, background.get_height()//2
		background.blit(picture, (x1 - picture.get_width() // 2, y1 - picture.get_height() // 2))
		
		x, y = self.screen.get_width()//2, self.screen.get_height()//2
		self.screen.blit(background,(x - background.get_width() // 2, y - background.get_height() // 2))
		hogo_frogo_teamo_logo_sound_path = '../audio/frog_quak-81741.mp3'
		hogo_frogo_teamo_logo_sound= pygame.mixer.Sound(hogo_frogo_teamo_logo_sound_path)
		hogo_frogo_teamo_logo_sound.play()
		pygame.display.flip()
		sleep(3.5)


		window = (700,500)
		background = pygame.Surface(window)

		myimage = pygame.image.load('../graphics/pygame_logo.png')
		picture = pygame.transform.scale(myimage, (600, 400))
		
		x1, y1 = background.get_width()//2, background.get_height()//2
		background.blit(picture, (x1 - picture.get_width() // 2, y1 - picture.get_height() // 2))
		
		x, y = self.screen.get_width()//2, self.screen.get_height()//2
		self.screen.blit(background,(x - background.get_width() // 2, y - background.get_height() // 2))
		pygame.display.flip()
		sleep(2.5)

	def start_the_game(self):
		player_name = 'Mr. Croak'
		# player_name = self.name_text_input.get_value()
		difficulty = self.difficulty_input.get_value()
		self.game.difficulty=difficulty
		
		print("obtížnost 1")
		print(difficulty)
		self.main_menu_music.stop()
		pygame_menu.events.EXIT
		self.game.overworld_bg_music.set_volume(self.music_volume)
		self.game.overworld_bg_music.play(loops = -1)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			
			self.screen.fill('grey')
			self.game.run(player_name,difficulty,self.music_volume)

			pygame.display.update()
			self.clock.tick(60)