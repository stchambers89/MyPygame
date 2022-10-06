import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        #player image/drawing
        self.image = pygame.image.load('graphics/test/ITGUY.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-64)

        #graphics setup
        self.import_player_assests()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.attack_sound = pygame.mixer.Sound('audio/attack.mp3')

        #Movement 
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None


        self.obstacle_sprites = obstacle_sprites

        #Player Timer limits multiple actions every ms to every few seconds
    def get_status(self):
        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:   
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
   
    def import_player_assests(self):
    #please note the strings below are the same spelling as the game files
    #refactoring the names will break the game and you will need to rename the 
    #files as well. 

        character_path = 'graphics/player/'
        self.animations = {
                #moving
            'up': [], 'down': [], 'left': [], 'right': [],
                #standing still
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                #attacking
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Movement input w,a,s,d or up,down,left,right
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
            
            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True 
                self.attack_time = pygame.time.get_ticks()
                self.attack_sound.play()
                print("attack")

            #magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True 
                self.attack_time = pygame.time.get_ticks()
                print('magic')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving Right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0: #moving top
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:#moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]

        #loop through index and reset to 0
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #select the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)