import pygame
from random import randint, uniform
from config import WINDOW_HEIGHT

class Meteor(pygame.sprite.Sprite):
    def __init__(self, resources, pos, groups):
        super().__init__(groups)
        self.original_surf = resources["meteor"]
        self.image = resources["meteor"]
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 5000
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5), 1)
        self.speed = randint(400,500)
        self.rotation_speed = randint(40, 50)
        self.rotation = 0
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()