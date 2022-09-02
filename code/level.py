from traceback import format_exc
import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm, Constraint
from enemy import Enemy
from poop import Poop
from fly import Fly
from ant import Ant
from dragonfly import Dragonfly
from wasp import Wasp
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels
from random import randint
from parachute_frog import ParachuteFrog
from tiles import AnimatedTile


class Level:
	#goal_image = '../graphics/misc/sandwich.png'
	def __init__(self,current_level,surface,create_overworld,change_coins,change_health,difficulty):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.level_border = 50
		self.difficulty = difficulty
		self.state = 'begin'
		self.player_name = "Mr. Croak"

		# audio 
		self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
		self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
		self.eat_sound = pygame.mixer.Sound('../audio/effects/eat.wav')
		self.croak_speak_sound = pygame.mixer.Sound('../audio/effects/croak.wav')
		self.fly_speak_sound = pygame.mixer.Sound('../audio/effects/bzzz.wav')

		# overworld connection 
		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		print("obtížnost")
		print(difficulty)
		if difficulty[0][0] == "Hard":
			self.fly_occurency_probability = level_data['flies_hard']
			self.dragonfly_occurency_probability = level_data['dragonflies_hard']
			self.wasp_occurency_probability = level_data['wasps_hard']
			self.parachute_frog_ocurency_probability = level_data['parachute_frog_hard']
		else:
			self.fly_occurency_probability = level_data['flies']
			self.dragonfly_occurency_probability = level_data['dragonflies']
			self.wasp_occurency_probability = level_data['wasps']
			self.parachute_frog_ocurency_probability = level_data['parachute_frog']

		# player 
		self.goal_image = level_data['goal_image']
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.boss = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout,change_health)
		self.killed_ants = 0
		self.killed_flies = 0

		# user interface 
		self.change_coins = change_coins

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# explosion particles 
		self.explosion_sprites = pygame.sprite.Group()

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		# grass setup 
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout,'grass')

		# crates 
		crate_layout = import_csv_layout(level_data['crates'])
		self.crate_sprites = self.create_tile_group(crate_layout,'crates')

		# coins 
		coin_layout = import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout,'coins')

		# foreground palms 
		fg_palm_layout = import_csv_layout(level_data['fg palms'])
		self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')

		# background palms 
		bg_palm_layout = import_csv_layout(level_data['bg palms'])
		self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

		# enemy 
		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

		# constraint 
		constraint_layout = import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

		# decoration 
		self.sky = Sky(8)
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(screen_height - 20,level_width)
		self.clouds = Clouds(400,level_width,30)

	def change_sounds_volume(self, new_volume):
		print("New volume")
		print(new_volume)
		self.coin_sound.set_volume(new_volume)
		self.stomp_sound.set_volume(new_volume)
		self.eat_sound.set_volume(new_volume)
		self.croak_speak_sound.set_volume(new_volume)
		self.fly_speak_sound.set_volume(new_volume)
		self.player.sprite.change_sounds_volume(new_volume)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
						
					if type == 'grass':
						grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
					
					if type == 'crates':
						sprite = Crate(tile_size,x,y)

					if type == 'coins':
						if val == '0': sprite = Coin(tile_size,x,y,'../graphics/coins/gold',5)
						if val == '1': sprite = Coin(tile_size,x,y,'../graphics/coins/silver',1)

					if type == 'fg palms':
						if val == '0': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_small',38)
						if val == '1': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_large',64)

					if type == 'bg palms':
						sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_bg',64)

					if type == 'enemies':
						if val == '0': sprite = Ant(tile_size,x,y)
						if val == '1': sprite = Fly(tile_size,x,y)
						if val == '2': sprite = Dragonfly(tile_size,x,y)
						if val == '3': sprite = Wasp(tile_size,x,y)
						

					if type == 'constraint':
						if val == '0': sprite = Constraint(tile_size,x,y,0)
						if val == '1': sprite = Constraint(tile_size,x,y,1)
						if val == '2': sprite = Constraint(tile_size,x,y,2)
						if val == '3': sprite = Constraint(tile_size,x,y,3)

					sprite_group.add(sprite)
		
		return sprite_group

	def player_setup(self,layout,change_health):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
					self.player.add(sprite)
				if val == '1':
					hat_surface = pygame.image.load(self.goal_image).convert_alpha()
					sprite = StaticTile(tile_size,x,y,hat_surface)
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if isinstance(enemy,Ant):
				collided_constraints = pygame.sprite.spritecollide(enemy,self.constraint_sprites,False)
				if collided_constraints:	
					for constraint in collided_constraints:
						#print(constraint.value)
						if constraint.value == 0:
							enemy.reverse()
							break
			if isinstance(enemy,Fly):
				collided_constraints = pygame.sprite.spritecollide(enemy,self.constraint_sprites,False)
				if collided_constraints:	
					for constraint in collided_constraints:
						#print(constraint.value)
						if constraint.value == 1:
							enemy.reverse()
							break
			if isinstance(enemy, Dragonfly):
				collided_constraints = pygame.sprite.spritecollide(enemy,self.constraint_sprites,False)
				if collided_constraints:	
					for constraint in collided_constraints:
						#print(constraint.value)
						if constraint.value == 2:
							enemy.reverse()
							break
				if(randint(0,999)<50):
					enemy.speed_y=-enemy.speed_y

			if isinstance(enemy,Wasp):
				collided_constraints = pygame.sprite.spritecollide(enemy,self.constraint_sprites,False)
				if collided_constraints:	
					for constraint in collided_constraints:
						#print(constraint.value)
						if constraint.value == 3:
							enemy.reverse()
							break

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.collision_rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.x < 0: 
					player.collision_rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.collision_rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.y > 0: 
					player.collision_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.collision_rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		player_speed = player.native_speed
		direction_x = player.direction.x

		if player_x < screen_width / 2.5 and direction_x < 0:
			self.world_shift = player_speed
			player.speed = 0
		elif player_x > screen_width - (screen_width / 2.5) and direction_x > 0:
			self.world_shift = -player_speed
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = player_speed

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			print("last death")
			print(self.difficulty)
			self.create_overworld(self.current_level,0,self.difficulty)
	
	def text_line_split(self,text_content):
		text_lines = []
		text_length = len(text_content)
		text_length_max = 60
		while (text_length>text_length_max):
			#Split the text, one with length 5 and the rest

			# WordWrap
			# If first 4 letters are not space it is ok
			# But if there are it is hard
			text_line = text_content[0:text_length_max]
			# Pokud je text_line dlouhej jako limit a v text_content jsou ještě další znaky, tak
			print("Podmínka 0 splněna")
			print(len(text_line))
			print(text_length_max)
			
			if(len(text_line)==text_length_max) and len(text_content[text_length_max:])>0:
				print("Podmínka 1 splněna")
				## Pokud nenajdu mezeru na konci daného ani na začátku řetězce následujícího
				if(text_content[text_length_max-1]!=" " and text_content[text_length_max]!=" "):
					### Tak musím text říznout v bodě poslední mezery v prvním (daném) řetězci
					i = 1
					while i < len(text_content):
						letter = text_line[-i]
						if(letter==" "):
							print("test")
							text_split_index = text_length_max-i
							text_line = text_line[0:text_split_index]

							text_content = text_content[text_split_index+1:]
							text_length = len(text_content)
							text_lines.append(text_line)
							break
						i+=1
				else:
					if (text_content[text_length_max]!=" "):
						text_content = text_content[text_length_max+1:]
					else:
						text_content = text_content[text_length_max:]
					text_length = len(text_content)
					text_lines.append(text_line)
			else:
				if(text_line[0]==" "):
					text_line = text_line[1:]
				text_content = text_content[text_length_max:]
				text_length = len(text_content)
				text_lines.append(text_line)
			print(text_line)
		if(text_content[0]==" "):
			text_content = text_content[1:]
		text_lines.append(text_content)

		return text_lines
		

	def view_dialog(self,text_content,image_path,dialog_sound=""):
		if dialog_sound != "":
			dialog_sound.play()
		next_state=self.state
		self.state = 'dialog'
		window = (700,500)
		background = pygame.Surface(window)
		background.fill((102, 187, 106))

		#Insert text
		text_lines = self.text_line_split(text_content)
		font = pygame.font.SysFont('Arial', 24)
		line_n = 1
		print("délka pole lajn")
		print(len(text_lines))
		for line in text_lines:
			text = font.render(line, True, pygame.color.Color('Black'))
			background.blit(text, (20, 20*line_n))
			line_n+=1

		myimage = pygame.image.load(image_path)
		imagerect = myimage.get_rect()
		picture = pygame.transform.scale(myimage, (280, 140))
		
		x1, y1 = background.get_width()//2, background.get_height()//2
		background.blit(picture, (x1 - picture.get_width() // 2, y1 - picture.get_height() // 2))
		
		x, y = self.display_surface.get_width()//2, self.display_surface.get_height()//2
		self.display_surface.blit(background,(x - background.get_width() // 2, y - background.get_height() // 2))

		pygame.display.flip()
		while self.state == 'dialog':
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.state = next_state
	def enter_dialog(self,dialog_type):
		match(dialog_type):
			case 'sad_frog':
				player_img = '../graphics/character/run/1.png'
				sad_frog_img = '../graphics/misc/sad_frog.png'
				self.view_dialog("Hello there! I'm "+self.player_name+"!",player_img,self.croak_speak_sound)
				self.view_dialog("Hello "+self.player_name+"! :(",sad_frog_img,self.croak_speak_sound)
				self.view_dialog("What's going on?",player_img,self.croak_speak_sound)
				self.view_dialog("My wife has prepared me my favourite salami sandwich for snack but evil flies have taken the control over it!",sad_frog_img,self.croak_speak_sound)
				self.view_dialog("Why don't you eat them?",player_img,self.croak_speak_sound)
				self.view_dialog("I'm allergic to flies! :(",sad_frog_img,self.croak_speak_sound)
				self.view_dialog("Could you help me save my sandwich?",sad_frog_img,self.croak_speak_sound)
				self.view_dialog("Of course!",player_img,self.croak_speak_sound)
			case 'flyking':
				player_img = '../graphics/character/run/1.png'
				flyking_img = '../graphics/bosses/flyking.jpg'
				self.view_dialog("Uaaaaaaah!",player_img,self.croak_speak_sound)
				self.view_dialog("Muhahahaaa! I'm the fly king. Stop touching my sandwich!",flyking_img,self.fly_speak_sound)
				self.view_dialog("This sandwich is not yours!",player_img,self.croak_speak_sound)
				self.view_dialog("If you think so fight for it!",flyking_img,self.fly_speak_sound)
			case 'chase_start':
				player_img = '../graphics/character/run/1.png'
				strong_frog_img = '../graphics/bosses/flyking.jpg'
				self.view_dialog("Give me that sandwich!",strong_frog_img,self.croak_speak_sound)
				self.view_dialog("No!",player_img,self.croak_speak_sound)
				self.view_dialog("I will hunt you down!",strong_frog_img,self.croak_speak_sound)
				
	def begin_bossfight(self,boss):
		match(boss):
			case 'flyking':
				#when the boss fight starts, a fly king will appear at the right side of the screen
				#image = '../graphics/bosses/flyking/idle'
				#x = 500
				#y = 300
				#self.flyking = Ant(tile_size,x,y)
				#self.flyking.draw(self.display_surface)
					#health, image and attributes
				#the game freezes
				self.state = 'boss_cutscene'
				self.enter_dialog("flyking")
				self.state = 'bossfight'
				# deletes fly constraints from map so that they can fly all over the screen
				for constraint in self.constraint_sprites:
					if constraint.value == 1:
						constraint.value = 0
				#cutscene

				#combat starts
					self.boss_x = screen_width-120
					self.boss_y = 200
					boss = AnimatedTile(tile_size,self.boss_x,self.boss_y,'../graphics/bosses/flyking/run')
					self.boss.add(boss)
					# It is needed to somehow fix situation when camera moves

					#the sandwich disappears and some platforms needed for combat movement will appear

					#the boss will start spawning flies in a different frequency and pattern

				#boss takes damage
					#health will change
					#platforms will change
					#same as "combat starts"
				
				#boss' health is 0
					#cutscene
					#level end

				



			
	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
			if self.current_level==0:
				self.enter_dialog('sad_frog')
			if self.current_level==1:
				if self.killed_flies>=25 and self.killed_ants>=8 and self.state != 'bossfight':
					print("stav hry")
					print(self.state)
					#self.create_overworld(self.current_level,self.new_max_level,self.difficulty)
					self.begin_bossfight('flyking')
			else:
				self.create_overworld(self.current_level,self.new_max_level,self.difficulty)
			
	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
		if collided_coins:
			self.coin_sound.play()
			for coin in collided_coins:
				self.change_coins(coin.value)

	def check_boss_collisions(self):
		boss_collisions = pygame.sprite.spritecollide(self.player.sprite,self.boss,False)
		if boss_collisions:
			for enemy in boss_collisions:
				self.eat_sound.play()

	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				player_native_width = self.player.sprite.native_width
				player_native_height = self.player.sprite.native_height
				if (self.player.sprite.facing_right and self.player.sprite.rect.left+player_native_width < enemy.rect.left and self.player.sprite.tongue_stick_out) or (not self.player.sprite.facing_right and self.player.sprite.rect.right-player_native_width > enemy.rect.right and self.player.sprite.tongue_stick_out):
					self.eat_sound.play()
					self.player.sprite.heal(enemy.healing_points)
					# self.player.sprite.direction.y = -3
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
					if isinstance(enemy,Ant):
						self.killed_ants += 1
					if isinstance(enemy,Fly):
						self.killed_flies += 1
				elif (self.player.sprite.rect.bottom-player_native_height > enemy.rect.bottom and self.player.sprite.tongue_stick_out_up):
					self.eat_sound.play()
					self.player.sprite.heal(enemy.healing_points)
					# self.player.sprite.direction.y = -3
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
					if isinstance(enemy,Ant):
						self.killed_ants += 1
					if isinstance(enemy,Fly):
						self.killed_flies += 1
				elif enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y > 1:
					self.stomp_sound.play()
					self.player.sprite.direction.y = -13
					if self.player.sprite.facing_right:
						self.player.sprite.move_direction_right = True
					else:
						self.player.sprite.move_direction_right = False
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
					if isinstance(enemy,Ant):
						self.killed_ants += 1
					if isinstance(enemy,Fly):
						self.killed_flies += 1
				else:
					self.player.sprite.get_damage(enemy.attack_damage)

	def run(self):
		# run the entire game / level 
		
		# sky 
		self.sky.draw(self.display_surface)
		self.clouds.draw(self.display_surface,self.world_shift)
		
		# background palms
		self.bg_palm_sprites.update(self.world_shift)
		self.bg_palm_sprites.draw(self.display_surface) 

		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)
		
		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)
		
		# goal
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		# enemy 
		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_sprites.draw(self.display_surface)
		self.explosion_sprites.update(self.world_shift)
		self.explosion_sprites.draw(self.display_surface)

		self.boss.update(self.world_shift)
		self.boss.draw(self.display_surface)

		# crate 
		self.crate_sprites.update(self.world_shift)
		self.crate_sprites.draw(self.display_surface)

		# grass
		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		# coins 
		self.coin_sprites.update(self.world_shift)
		self.coin_sprites.draw(self.display_surface)

		# foreground palms
		self.fg_palm_sprites.update(self.world_shift)
		self.fg_palm_sprites.draw(self.display_surface)

		# player sprites
		self.player.update()
		self.horizontal_movement_collision()
		
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		if self.state != 'bossfight':
			self.scroll_x()
		else:
			if(self.goal.sprite.rect.centerx < (screen_width) / 2 - 5):
				self.world_shift = 10
				self.player.sprite.speed = 10
			elif(self.goal.sprite.rect.centerx > (screen_width) / 2 + 5):
				self.world_shift = -10
				self.player.sprite.speed = -10
			else:
				self.world_shift = 0
				self.player.sprite.speed = self.player.sprite.native_speed
		self.player.draw(self.display_surface)

		self.check_death()
		self.check_win()

		self.check_coin_collisions()
		self.check_enemy_collisions()
		self.check_boss_collisions()

		# water 
		self.water.draw(self.display_surface,self.world_shift)

		if(randint(0,999)<self.fly_occurency_probability): self.enemy_sprites.add(Fly(tile_size,screen_width,randint(self.level_border,screen_height-self.level_border)))
		if self.state == 'bossfight':
			if(randint(0,999)<self.fly_occurency_probability*5): self.enemy_sprites.add(Poop(tile_size,self.boss_x,self.boss_y,randint(150,210),12))
		if(randint(0,999)<self.dragonfly_occurency_probability): self.enemy_sprites.add(Dragonfly(tile_size,screen_width,randint(self.level_border,screen_height-self.level_border)))
		if(randint(0,999)<self.wasp_occurency_probability): self.enemy_sprites.add(Wasp(tile_size,screen_width,randint(self.level_border,screen_height-self.level_border)))
		if(randint(0,999)<self.parachute_frog_ocurency_probability): self.enemy_sprites.add(ParachuteFrog(tile_size,randint(0, screen_width),0))
		
		if self.state == 'begin':
			self.state = 'running'
			if self.current_level==2:
				self.enter_dialog("chase_start")