from hashlib import new
from typing_extensions import Self
import pygame, sys
import pygame_menu
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI
from game import Game


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game(screen)

main_menu_music = pygame.mixer.Sound('../audio/magnetic_b-ing.mp3')
music_volume = 0.5
main_menu_music.set_volume(music_volume)

def start_the_game():
	player_name = name_text_input.get_value()
	difficulty = difficulty_input.get_value()
	main_menu_music.stop()
	pygame_menu.events.EXIT
	game.overworld_bg_music.play(loops = -1)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		screen.fill('grey')
		game.run(player_name,difficulty,music)

		pygame.display.update()
		clock.tick(60)

def change_music_volume(new_volume):
	music_volume = new_volume
	main_menu_music.set_volume(music_volume)


menu = pygame_menu.Menu('Hogo Frogo', 400, 300,
                       theme=pygame_menu.themes.THEME_GREEN)

name_text_input = menu.add.text_input('PlayerName: ', default='Mr. Croak')
difficulty_input = menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
volume_slider = menu.add.range_slider('Volume', music_volume, [0, 1], 1, change_music_volume)
main_menu_music.play(loops = -1)
menu.mainloop(screen)
