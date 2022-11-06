import pygame
from config import *
import math, random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey('black')
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.width = self.height = TILE_SIZE
        self.x_change, self.y_change = 0, 0
        self.facing = 'down'

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = self.y_change = 0
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED * self.game.deltatime
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED * self.game.deltatime
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED * self.game.deltatime
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED * self.game.deltatime
            self.facing = 'down'
    
    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if direction == 'x': 
            if hits :
                if self.x_change > 0: self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0: self.rect.x = hits[0].rect.right 
        if direction == 'y':
            if hits :
                if self.y_change > 0: self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0: self.rect.y = hits[0].rect.bottom


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        super().__init__(self.groups)

        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.width, self.height = TILE_SIZE, TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.width = self.height = TILE_SIZE
        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y