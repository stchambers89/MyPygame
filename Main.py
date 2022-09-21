import imp
import pygame
from sys import exit

pygame.init()

# Basic Game Settings
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Etharis Island')
font = pygame.font.Font('font/RetGanon.ttf', 50)

clock =  pygame.time.Clock()

skySurface= pygame.image.load('graphics/sky.png')
groundSurface = pygame.image.load('graphics/ground.png')
fontSurface = font.render('Test game', False, 'ForestGreen')

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(skySurface, (200,0))
    screen.blit(groundSurface, (0,300))
    screen.blit(fontSurface, (300, 50))
    
    pygame.display.update()
    clock.tick(60) #Capped game speed