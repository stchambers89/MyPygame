import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    
    def __init__(self):

        #get display serface
        self.display_surface = pygame.display.get_surface()

        #Sprite Group Setup 
        self.visable_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        #Sprite set up
        self.create_map()
    
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y), [self.visable_sprites, self.obstacles_sprites])
                if col == 'p':
                    Player((x,y), [self.visable_sprites])
            
            



    def run(self):
        self.visable_sprites.draw(self.display_surface)