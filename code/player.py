from tkinter.tix import Tree
import pygame 
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles,change_health,sounds_volume=0.5,graphics="default"):
		super().__init__()
		self.character_path = '../graphics/character/'
		if graphics == "different":
			self.character_path = '../graphics/character/different/'
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.tongue_stick_out = False
		self.tongue_stick_out_timeout = 0
		self.stickout_charging_time = 50
		self.native_width = 48
		
		
		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 4
		self.native_speed = 4
		self.gravity = 0.8
		self.jump_speed = 5
		self.jump_energy = 0
		self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))
		self.jump_energy_limit = 48

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		# health management
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

		# audio 
		self.jump_sound = pygame.mixer.Sound('../audio/effects/jump2.mp3')
		self.jump_sound.set_volume(sounds_volume)
		self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')
		self.hit_sound.set_volume(sounds_volume)

	def change_sounds_volume(self,new_volume):
		self.jump_sound.set_volume(new_volume)
		self.hit_sound.set_volume(new_volume)

	def import_character_assets(self):
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'tongue_stick_out':[]}

		for animation in self.animations.keys():
			full_path = self.character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder(self.character_path+'dust_particles/run')

	def animate(self):
		animation = self.animations[self.status]
		image = animation[int(self.frame_index)]
		if not self.facing_right:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image
		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)	


		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		if self.facing_right:
			self.image = image
			self.rect.bottomleft = self.collision_rect.bottomleft
		else:
			self.rect.bottomright = self.collision_rect.bottomright

		if self.invincible:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)	

	def run_dust_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	def get_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_s] and self.on_ground:
			self.facing_right = False
		if keys[pygame.K_l] and self.on_ground:
			self.facing_right = True
		if keys[pygame.K_s] and keys[pygame.K_SPACE] and self.on_ground:
			if self.jump_energy<self.jump_energy_limit:
				self.jump_energy += 1
		elif self.on_ground==False and self.facing_right==False:
			self.direction.x = -1
		
		elif keys[pygame.K_l] and keys[pygame.K_SPACE] and self.on_ground:
			if self.jump_energy<self.jump_energy_limit:
				self.jump_energy += 1
		elif self.on_ground==False and self.facing_right==True:
			self.direction.x = 1
		elif keys[pygame.K_SPACE]:
			self.jump_energy = 0
		elif self.jump_energy>0:
			self.create_jump_particles(self.rect.midbottom)
			self.jump()
			if self.jump_energy>5:
				self.native_speed = 6
			elif self.jump_energy>10:
				self.native_speed = 8
			else:
				self.native_speed = 4
			self.jump_energy = 0
		else:
			self.direction.x = 0
			self.jump_energy = 0
		if keys[pygame.K_k] and self.tongue_stick_out_timeout==0:
			self.tongue_stick_out = True
			self.tongue_stick_out_timeout = self.stickout_charging_time+20
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.state = 'quick_menu'
					window = (400,400)
					background = pygame.Surface(window)
					background.fill((255, 255, 255))
					font = pygame.font.SysFont('Arial', 24)
					text = font.render("Quick Menu", True, pygame.color.Color('Black'))
					background.blit(text, (20, 20))

					myimage = pygame.image.load(self.character_path+'run/1.png')
					imagerect = myimage.get_rect()
					picture = pygame.transform.scale(myimage, (280, 100))
					background.blit(picture, (200,200))
					
					self.display_surface.blit(background,(0,0))

					pygame.display.flip()
					while self.state == 'quick_menu':
						for event in pygame.event.get():
							if event.type == pygame.KEYDOWN:
								if event.key == pygame.K_ESCAPE:
									self.state = 'end'

	def get_status(self):
		if self.tongue_stick_out:
			self.status = 'tongue_stick_out'
		elif self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.collision_rect.y += self.direction.y

	def jump(self):
			self.direction.y = -self.jump_speed - self.jump_energy/3
			self.jump_sound.play()
			
	def heal(self, healing_points):
			self.change_health(healing_points)

	def get_damage(self, damage):
		if not self.invincible:
			self.hit_sound.play()
			self.change_health(-damage)
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return 255
		else: return 0

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.run_dust_animation()
		self.invincibility_timer()
		self.wave_value()
		
		if(self.tongue_stick_out_timeout<=self.stickout_charging_time):
			self.tongue_stick_out=False
		if(self.tongue_stick_out_timeout>0):
			self.tongue_stick_out_timeout-=1
		else:
			self.tongue_stick_out=False
		