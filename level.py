import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from menu import Menu

class Level:
    
    def __init__(self):

        #get display serface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        #Sprite Group Setup 
        self.visable_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #Sprite set up
        self.create_map()

        #UI
        self.ui = UI()
        self.menu = Menu(self.player)

        #particles
        self.animation_player = AnimationPlayer()
    
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('map\map_etharis_boundary.csv'),
            'grass' : import_csv_layout('map\map_Grass.csv'),
            'object' : import_csv_layout('map\map_Objects.csv'),
            'entities' : import_csv_layout('map\map_etharis_entities.csv')
        }

        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }
        
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisable')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),
                            [self.visable_sprites, 
                            self.obstacle_sprites, 
                            self.attackable_sprites], 
                            'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visable_sprites, self.obstacle_sprites], 'object', surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    [self.visable_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                if col == '390' : monster_name = 'bamboo'
                                elif col == '391' : monster_name = 'spirit'
                                elif col == '392' : monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Enemy(monster_name, (x,y), 
                                [self.visable_sprites, self.attackable_sprites], 
                                self.obstacle_sprites,
                                self.damage_player,
                                self.trigger_death_particles,
                                self.add_exp)
                            
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visable_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos, [self.visable_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
    
    def damage_player(self, amount, attack_type):
        if self.player.vunerable:
            self.player.health -= amount
            self.player.vunerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visable_sprites])
        
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visable_sprites)
    
    def add_exp(self, amount):
        self.player.exp += amount
    
    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visable_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.menu.display()
        else:
            self.visable_sprites.update()
            self.visable_sprites.enemy_update(self.player)
            self.player_attack_logic()
            #run game
        
        
        
        
        
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #CREATE MAIN FLOOR IMAGE
        self.floor_surf = pygame.image.load(MAP).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    
    def custom_draw(self, player):

        #getting offest
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
                enemy.enemy_update(player)