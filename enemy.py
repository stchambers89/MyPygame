import pygame
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups):
        super().__init__(groups)

        self.sprite_type = 'enemy'

        #enemy Graphics
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)