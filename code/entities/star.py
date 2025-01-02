import pygame
from random import randint
from config import WINDOW_WIDTH, WINDOW_HEIGHT 

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, resources):
        super().__init__(groups)
        self.image = resources["star"]
        self.rect = self.image.get_frect(topleft=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        self.speed = randint(10, 20)

    def update(self,dt):
        self.rect.centery += self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0 
            self.rect.x = randint(0, WINDOW_WIDTH)