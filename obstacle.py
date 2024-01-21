import pygame
from random import randint, choice
import sys

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('./graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('./graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.y_pos = 210
        
        else:
            snail_1 = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('./graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), self.y_pos))

    def animation_state(self):
        if self.y_pos == 300: self.animation_index += 0.08
        else: self.animation_index += 0.14
        self.image = self.frames[int(self.animation_index) % 2]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self, score):
        self.animation_state()
        self.rect.x -= (6 + score // 6)
        self.destroy()