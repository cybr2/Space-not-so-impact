import pygame
from random import randint
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from entities.laser import Laser

class Enemy(pygame.sprite.Sprite):
    def __init__(self, resources, all_sprite, pos, laser_sprite, groups):
        super().__init__(groups)
        
        # Load and resize the enemy image
        self.resize_image = pygame.transform.scale(resources['enemy'], (112, 75))
        self.resize_image = pygame.transform.rotate(self.resize_image, 180)
        self.original_surf = self.resize_image
        self.image = self.resize_image
        self.rect = self.image.get_frect(center = pos)
        
        # Movement and shooting properties
        self.direction = pygame.math.Vector2(0, 1)  # Move downward
        self.speed = randint(40, 80)  # Speed in pixels/second
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 2000  # Shoot laser every 2000ms (2 seconds)
        
        # Resource references
        self.resources = resources
        self.all_sprites = all_sprite
        self.laser_sprites = laser_sprite

        self.owner = "enemy"  # This defines that the laser belongs to the enemy
        

    def laser_time(self):
        """Handle laser shooting cooldown."""
        current_time = pygame.time.get_ticks()
        if current_time - self.laser_shoot_time >= self.cooldown_duration:
            self.can_shoot = True  # Allow shooting after the cooldown duration

    def shoot_laser(self):
        """Shoot a laser from the enemy."""
        # Create the laser object, with the correct 'owner' and positions
        Laser(self.resources, self.rect.midbottom, self.owner, (self.all_sprites, self.laser_sprites))
        self.laser_shoot_time = pygame.time.get_ticks()
        self.can_shoot = False  # Prevent shooting until the cooldown is over
        self.resources["laser_sound"].play()  # Play laser sound

    def update(self, dt):
        """Update enemy movement and shooting behavior."""
        # Move downward
        self.rect.midtop += self.direction * self.speed * dt
        
        # Check if the enemy is ready to shoot a laser
        if self.can_shoot:
            self.shoot_laser()
        
        # Update the cooldown timer
        self.laser_time()
        
        # Remove the enemy if it goes out of the screen
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
