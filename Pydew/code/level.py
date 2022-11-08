import pygame
from player import Player
from settings import *
from overlay import Overlay
from sprites import Generic

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)
    
    def setup(self):
        Generic(
            (0, 0),
            pygame.image.load('graphics/world/ground.png').convert_alpha(),
            self.all_sprites
        )
        self.player = Player((640, 360), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw()
        self.all_sprites.update(dt)

        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def customize_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)