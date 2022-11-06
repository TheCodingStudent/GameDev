import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans', 32)
        self.running = True
        self.deltatime = 0

        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
    
    def create_tilemap(self):
         for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B': Block(self, j, i)
                elif column == 'P': Player(self, j, i)
    
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.create_tilemap()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    
    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        miliseconds = self.clock.tick(FPS) / 1000
        pygame.display.set_caption(f'FPS: {1/miliseconds:.0f}')
        self.deltatime = miliseconds
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
    
    def intro(self):
        ...
    
    def game_over(self):
        ...


game = Game()
game.intro()
game.new()

while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()