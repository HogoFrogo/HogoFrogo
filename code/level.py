import pygame 
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm, Constraint
from enemy import Enemy
from fly import Fly
from ant import Ant
from dragonfly import Dragonfly
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels
from random import randint

from wasp import Wasp

class Level:
	#goal_image = '../graphics/misc/sandwich.png'
	def __init__(self,current_level,surface,create_overworld,change_coins,change_health,difficulty):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.level_border = 50
		self.difficulty = difficulty

		# audio 
		self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
		self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
		self.eat_sound = pygame.mixer.Sound('../audio/effects/eat.wav')

		# overworld connection 
		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		print("obtížnost")
		print(difficulty)
		if difficulty[0][0] == "Hard":
			self.fly_occurency_probability = level_data['flies-hard']
			self.dragonfly_occurency_probability = level_data['dragonflies-hard']
			self.wasp_occurency_probability = level_data['wasps-hard']
		else:
			self.fly_occurency_probability = level_data['flies']
			self.dragonfly_occurency_probability = level_data['dragonflies']
			self.wasp_occurency_probability = level_data['wasps']

		# player 
		self.goal_image = level_data['goal_image']
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
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
						

					if type == 'constraint':
						if val == '0': sprite = Constraint(tile_size,x,y,0)
						if val == '1': sprite = Constraint(tile_size,x,y,1)
						if val == '2': sprite = Constraint(tile_size,x,y,2)

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
				if(randint(0,999)<50):
					enemy.speed_y=-enemy.speed_y

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
			
	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
			if self.current_level==1:
				if self.killed_flies>=25 and self.killed_ants>=8:
					self.create_overworld(self.current_level,self.new_max_level,self.difficulty)
			else:
				self.create_overworld(self.current_level,self.new_max_level,self.difficulty)
			
	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
		if collided_coins:
			self.coin_sound.play()
			for coin in collided_coins:
				self.change_coins(coin.value)

	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				player_native_width = self.player.sprite.native_width
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
				elif enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					self.stomp_sound.play()
					# self.player.sprite.direction.y = -3
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
		
		self.scroll_x()
		self.player.draw(self.display_surface)

		self.check_death()
		self.check_win()

		self.check_coin_collisions()
		self.check_enemy_collisions()

		# water 
		self.water.draw(self.display_surface,self.world_shift)

		if(randint(0,999)<self.fly_occurency_probability): self.enemy_sprites.add(Fly(tile_size,screen_width,randint(self.level_border,screen_height-self.level_border)))
		if(randint(0,999)<self.dragonfly_occurency_probability): self.enemy_sprites.add(Dragonfly(tile_size,screen_width,randint(self.level_border,screen_height-self.level_border)))
		if(randint(0,999)<self.wasp_occurency_probability): self.enemy_sprites.add(Wasp(tile_size,screen_width,randint(self.level_border,screen_height-self.level_border)))