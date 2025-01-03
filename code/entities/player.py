import pygame
from os.path import join
from random import randint, uniform
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from entities.laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, resources, all_sprites, laser_sprite):
        super().__init__(groups)
        self.original_surf = resources["player"]
        self.image = resources["player"]
        self.rect = self.image.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 10))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 600
        self.rotation = 0
        self.scale = 1.0
        self.resources = resources
        self.all_sprites = all_sprites
        self.laser_sprites = laser_sprite
        self.owner = "player"
        

    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        # Prevent player from going beyond the window boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

        if (pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]) and self.can_shoot:
            Laser(self.resources, self.rect.midtop, self.owner, (self.all_sprites, self.laser_sprites)) 
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            self.resources["laser_sound"].play()

        self.laser_time()

            # Tilting and scaling logic
        self.update_transform()       
    
    def update_transform(self):
        if self.direction.x != 0:
            self.rotation = -15 * self.direction.x
        else:
            self.rotation = 0
            
        # Adjust scale based on vertical movement
        if self.direction.y < 0:  # Moving forward
            self.scale = 1.1
        elif self.direction.y > 0:  # Moving backward
            self.scale = 0.9 
        else:
            self.scale = 1.0  # Reset scale when stationary
            
        # Apply transformations
        transformed_surf = pygame.transform.rotozoom(self.original_surf, self.rotation, self.scale)
        self.image = transformed_surf
        self.rect = self.image.get_frect(center=self.rect.center)  # Keep the sprite centered