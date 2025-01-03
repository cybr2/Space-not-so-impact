import pygame
from entities.explosion import AnimatedExplosion

def collision(resources, player, meteor_sprites, laser_sprites, all_sprites, enemy_sprites, game_active):
    
    # Handle collision of player with meteors
    craft_collision_sprites = pygame.sprite.spritecollide(player, enemy_sprites, True, collided=pygame.sprite.collide_mask)
    # Handle collision and trigger explosion
    if craft_collision_sprites:
        print("Player collided with an enemy!")
        resources["explosion_sound"].play()
        resources["game_music"].stop()
        game_active = False  # End the game here
    
    craft_meteor_collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, collided=pygame.sprite.collide_mask)
    # Handle collision and trigger explosion
    if craft_meteor_collision_sprites:
        resources["explosion_sound"].play()
        resources["game_music"].stop()
        game_active = False  # End the game here

    # Handle laser collisions with meteors, enemies, and player
    for laser in laser_sprites:
        # Laser from enemy collides with player
        if laser.owner == "enemy":
            if pygame.sprite.collide_mask(laser, player):  # Check if laser collides with player
                resources["explosion_sound"].play()
                resources["game_music"].stop()
                game_active = False
                break  # End loop if the player is hit by an enemy laser

        # Laser from player collides with enemies
        if laser.owner == "player":
            # Handle laser collisions with meteors (only player lasers destroy meteors)
            collided_meteors = pygame.sprite.spritecollide(laser, meteor_sprites, True)
            if collided_meteors:
                laser.kill()  # Destroy the laser
                AnimatedExplosion(resources["explosion"], laser.rect.midtop, all_sprites)
                resources["explosion_sound"].play()
            
            print("Enemy SPOTTED")
            # Handle enemy death
            collided_enemies = pygame.sprite.spritecollide(laser, enemy_sprites, True)
            if collided_enemies:
                print(f"Collided with {len(collided_enemies)} enemies")
                laser.kill()  # Destroy the laser
                for enemy in collided_enemies:
                    enemy.kill()  # Properly remove each enemy from the group
                    AnimatedExplosion(resources["explosion"], enemy.rect.center, all_sprites)  # Explosion effect
                    resources["explosion_sound"].play()


    return game_active
