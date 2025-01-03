import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,resources, pos, owner, groups):
        super().__init__(groups)
        self.image = resources["laser"]
        self.rect = self.image.get_frect(midbottom = pos)
        self.laser_speed = 500 if owner == 'player' else 300
        self.owner = owner

        self.direction = -1 if owner == "player" else 1

    def update(self, dt):
        self.rect.centery += self.laser_speed * self.direction * dt
        if self.rect.top > pygame.display.get_surface().get_height() or self.rect.bottom < 0:
            self.kill()