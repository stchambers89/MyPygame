from distutils.util import convert_path
import imp
import pygame
from sys import exit

pygame.init()

# Basic Game Settings
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Etharis Island')
font = pygame.font.Font('font/RetGanon.ttf', 50)

clock =  pygame.time.Clock()

sky_surface= pygame.image.load('graphics/sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
font_surface = font.render('Test game', False, 'ForestGreen', 'white')

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600,300))


player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
Player_rect = player_surface.get_rect(midbottom = (80,300))

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(sky_surface,     (0,0))
    screen.blit(ground_surface,  (0,300))
    screen.blit(font_surface,    (300, 50))
    screen.blit(player_surface, Player_rect)
    if snail_rect.left <= -100:
        snail_rect.left = 820
    else:
        snail_rect.left -= 3
    screen.blit(snail_surface, snail_rect)
    
    pygame.display.update()
    clock.tick(60) #Capped game speed