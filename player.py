import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)

        #player image/drawing
        self.image = pygame.image.load('graphics/player/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)

        #graphics setup
        self.import_player_assests()
        self.status = 'down'
        self.attack_sound = pygame.mixer.Sound('audio/attack.mp3')

        #Movement 
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0 
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_weapon_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_magic_cooldown = 200


        #Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 10
        
        #damage timer
        self.vunerable = True
        self.hurt_time = None
        self.invunerablity_duration = 500

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
                self.create_attack()
                self.attack_sound.play()
                print("attack")

            #magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True 
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']

                self.create_magic(style, strength, cost)
                

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < int(len(list(weapon_data.keys())) -1):
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                print ('weapon switch')

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < int(len(list(magic_data.keys())) -1):
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]
                print ('magic switch')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_weapon_cooldown:
                self.can_switch_weapon = True
        
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_magic_cooldown:
                self.can_switch_magic = True
        
        if not self.vunerable:
            if current_time - self.hurt_time >= self.invunerablity_duration:
                self.vunerable = True

    def animate(self):
        animation = self.animations[self.status]

        #loop through index and reset to 0
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #select the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker damage effect
        if not self.vunerable:
            alpha  = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def get_full_weapon_damage(self):
        base_damage = self.stats.get('attack')
        weapon_damage = weapon_data[self.weapon]['damage']

        return base_damage + weapon_damage

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)