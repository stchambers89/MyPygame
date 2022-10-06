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
            self.status = self.status + '_idle'
   
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
        keys = pygame.key.get_pressed()

        # Movement input w,a,s,d or up,down,left,right
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        #attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True 
            self.attack_time = pygame.time.get_ticks()
            print("attack")

        #magic input
        if keys[pygame.K_LCTRL] and not self.attacking:
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

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.move(self.speed)