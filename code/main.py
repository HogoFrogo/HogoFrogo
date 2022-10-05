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
		option = f.readline().split(" = ")
		music_volume = float(option[1])
		option = f.readline().split(" = ")
		sounds_volume = float(option[1])
	return {"music_volume": music_volume, "sounds_volume": sounds_volume}

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

def toggle_fullscreen():
	print('Will toggle fullscreen')

settings=load_settings_from_file()
music_volume = settings["music_volume"]
sounds_volume = settings["sounds_volume"]

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
	widget_font=font
)

# Pygame setup
pygame.init()
pygame.display.set_caption("Hogo Frogo")
screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN)
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

main_menu = pygame_menu.Menu('Hogo Frogo', screen_width, screen_height,
                       theme=THEME_HOGO_FROGO)
play_menu = pygame_menu.Menu('Play', screen_width, screen_height,
                       theme=THEME_HOGO_FROGO)
name_text_input = play_menu.add.text_input('PlayerName: ', default='Mr. Croak')
difficulty_input = play_menu.add.selector('Difficulty :', [('Toad', 1), ('Frog', 2)])
play_menu.add.button('Play', start_the_game)

credits_menu = pygame_menu.Menu('Credits', screen_width, screen_height,
                       theme=THEME_HOGO_FROGO)
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

settings_menu = pygame_menu.Menu('Settings', screen_width, screen_height,
                       theme=THEME_HOGO_FROGO)
volume_slider = settings_menu.add.range_slider('Music Volume', music_volume, [0, 1], 1, change_music_volume)
sounds_volume_slider = settings_menu.add.range_slider('Sounds Volume', sounds_volume, [0, 1], 1, change_sounds_volume)
full_screen_checkbox = settings_menu.add.button('Fullscreen', toggle_fullscreen)

main_menu.add.menu_link(play_menu, 'Play')
main_menu.add.button('Play', play_menu)
main_menu.add.menu_link(settings_menu, 'Settings')
main_menu.add.button('Settings', settings_menu)
main_menu.add.menu_link(credits_menu, 'Credits')
main_menu.add.button('Credits', credits_menu)
main_menu.add.button('Quit', pygame_menu.events.EXIT)
main_menu_music.play(loops = -1)
main_menu.mainloop(screen)