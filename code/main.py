from typing_extensions import Self
import pygame, sys
import pygame_menu
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI
from game import Game

def load_settings_from_file():
	with open('settings.conf', 'r') as f:
		#music_volume = float(f.read())
		#sounds_volume = float(f.read())
		music_volume = float(0)
		sounds_volume = float(0)
	return {"music_volume": music_volume, "sounds_volume": sounds_volume}

settings=load_settings_from_file()
music_volume = settings["music_volume"]
sounds_volume = settings["sounds_volume"]

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

load_settings_from_file()
game = Game(screen, music_volume, sounds_volume)

main_menu_music = pygame.mixer.Sound('../audio/magnetic_b-ing.mp3')
main_menu_music.set_volume(music_volume)

def start_the_game():
	player_name = name_text_input.get_value()
	difficulty = difficulty_input.get_value()
	game.difficulty=difficulty
	
	print("obtížnost 1")
	print(difficulty)
	main_menu_music.stop()
	pygame_menu.events.EXIT
	game.overworld_bg_music.set_volume(music_volume)
	game.overworld_bg_music.play(loops = -1)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		screen.fill('grey')
		game.run(player_name,difficulty,music_volume)

		pygame.display.update()
		clock.tick(60)

#settings saving
def save_settings_into_file():
	with open('settings.conf', 'w') as f:
		f.write("music_volume = " + str(game.music_volume) + "\n")
		f.write("sounds_volume = " + str(game.sounds_volume) + "\n")

def change_music_volume(new_volume):
	game.change_music_volume(new_volume)
	main_menu_music.set_volume(game.music_volume)
	save_settings_into_file()

def change_sounds_volume(new_volume):
	game.change_sounds_volume(new_volume)	
	save_settings_into_file()

main_menu = pygame_menu.Menu('Hogo Frogo', screen_width, screen_height,
                       theme=pygame_menu.themes.THEME_GREEN)

credits_menu = pygame_menu.Menu('Credits', screen_width, screen_height,
                       theme=pygame_menu.themes.THEME_GREEN)
credits_menu.add.label("Hello World")

name_text_input = main_menu.add.text_input('PlayerName: ', default='Mr. Croak')
difficulty_input = main_menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
main_menu.add.button('Play', start_the_game)
main_menu.add.button('Quit', pygame_menu.events.EXIT)
volume_slider = main_menu.add.range_slider('Volume', music_volume, [0, 1], 1, change_music_volume)
sounds_volume_slider = main_menu.add.range_slider('Sounds Volume', sounds_volume, [0, 1], 1, change_sounds_volume)
main_menu.add.menu_link(credits_menu, 'Credits')
main_menu.add.button('Credits', credits_menu)
main_menu_music.play(loops = -1)
main_menu.mainloop(screen)