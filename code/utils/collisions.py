import pygame
from entities.explosion import AnimatedExplosion

def collision(resources,player, meteor_sprites, laser_sprites, all_sprites, game_active):
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, collided = pygame.sprite.collide_mask)

    if collision_sprites:
        resources["game_music"].stop()
        game_active = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)

        if collided_sprites:
            laser.kill()
            AnimatedExplosion(resources["explosion"],laser.rect.midtop, all_sprites )
            resources["explosion_sound"].play()
    
    return game_active
