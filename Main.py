import imp
import pygame
from sys import exit

pygame.init()

# Basic Game Settings
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Etharis Island')

clock =  pygame.time.Clock()

testSurface = pygame.Surface((100,200))
testSurface.fill('ForestGreen')


# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(testSurface,(350,0))

    pygame.display.update()
    clock.tick(60) #Capped game speed