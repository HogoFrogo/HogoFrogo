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
def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
	main_menu_music.stop()
	pygame_menu.events.EXIT
	game.overworld_bg_music.play(loops = -1)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		screen.fill('grey')
		game.run()

		pygame.display.update()
		clock.tick(60)

menu = pygame_menu.Menu('Hogo Frogo', 400, 300,
                       theme=pygame_menu.themes.THEME_GREEN)

menu.add.text_input('PlayerName: ', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
main_menu_music.play(loops = -1)
menu.mainloop(screen)

