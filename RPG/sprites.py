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
        self.animation_loop = 0

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.sprites = {
            'down': [
                self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height),
            ],
            'up': [
                self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height),
            ],
            'left': [
                self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height),
            ],
            'right': [
                self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height),
            ]
        }
    
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
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
    
    def animate(self):
        if (self.x_change or self.y_change) == 0: self.animation_loop = 0
        else: self.animation_loop = (self.animation_loop + self.game.deltatime / 0.1) % 3
        self.image = self.sprites[self.facing][int(self.animation_loop)]

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False


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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        super().__init__(self.groups)

        self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
        self.width = self.height = TILE_SIZE

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(7, 15)

        self.x_change, self.y_change = 0, 0
        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.sprites = {
            'left': [
                self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height),
            ],
            'right': [
                self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height),
            ]
        }
    
    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = self.y_change = 0
    
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED * self.game.deltatime
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel: self.facing = 'right'
        elif self.facing == 'right':
            self.x_change += ENEMY_SPEED * self.game.deltatime
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel: self.facing = 'left'
        
    def animate(self):
        if (self.x_change or self.y_change) == 0: self.animation_loop = 0
        self.image = self.sprites[self.facing][int(self.animation_loop)]
        self.animation_loop = (self.animation_loop + self.game.deltatime / 0.1) % 3