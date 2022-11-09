import pygame, sys 
from settings import *
from debug import debug
from level import Level

class Game:
    def __init__(self):
        
        #Game Setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.title = pygame.display.set_caption('Elantris Island')
        self.clock = pygame.time.Clock()
        # self.background_music = pygame.mixer.Sound('main_gameplay.mp3')
        # self.background_music.set_volume(0.25)
        # self.background_music.play(loops = -1)
        
        self.level = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            #debug()
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()