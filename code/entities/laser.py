import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,resources, pos, *groups):
        super().__init__(*groups)
        self.image = resources["laser"]
        self.rect = self.image.get_frect(midbottom = pos)
        self.laser_speed = 500

    def update(self, dt):
        self.rect.centery -= self.laser_speed * dt
        if self.rect.bottom < 0:
            self.kill()