import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups, )
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 10))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        # Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 600
        # Rotation and scaling
        self.rotation = 0  # Rotation angle
        self.scale = 1.0   # Current scale factor

        #mask
        # self.mask = pygame.mask.from_surface(self.image) 
  

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

        if (pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]) and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites)) 
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sounds.play()

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

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        self.speed = randint(10, 20)

    def update(self, dt):
        self.rect.centery += self.speed * dt  # Move stars downwards
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0  # Reset to top when they go off-screen
            self.rect.x = randint(0, WINDOW_WIDTH)  # Randomize X position

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)


    def update(self, dt):
        self.rect.centery -= 400 * dt  # Move the laser upward
        if self.rect.bottom < 0:  # Remove the laser if it goes off-screen
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0


    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        #rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update (self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

# collisions 
def collisions():
    global running
    collision_sprites =  pygame.sprite.spritecollide(player, meteor_sprites, True, collided=pygame.sprite.collide_mask)
    if collision_sprites:    
        running = False
        game_over()

    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sounds.play()

def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, 'white')
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, 100))
    display_surface.blit(text_surf, text_rect)

    pygame.draw.rect(display_surface, 'white', text_rect.inflate(20,10).move(0,-8) , 5, 10)

def game_over():
    # Display the game over screen
    game_music.stop()
    game_over_music.play()
    game_over_font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 60)
    text_surf = game_over_font.render("Game Over", True, 'white')
    text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
    display_surface.blit(text_surf, text_rect)
    
    score_surf = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40).render(f"Score: {pygame.time.get_ticks() // 1000}", True, 'white')
    score_rect = score_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
    display_surface.blit(score_surf, score_rect)

    restart_text = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 30).render("Press 'R' to Restart or 'Q' to Quit", True, 'white')
    restart_rect = restart_text.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
    display_surface.blit(restart_text, restart_rect)

    pygame.display.update()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    game_over_music.stop()
                    main_game_loop()  # Restart the game
                    waiting_for_input = False

def main_menu():
    # Display the main menu screen
    game_menu_music.play(loops= -1)
    main_menu_font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 60)
    text_surf = main_menu_font.render("Space Shooter", True, 'white')
    text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
    display_surface.blit(text_surf, text_rect)
    
    start_text = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40).render("Press 'Enter' to Start", True, 'white')
    start_rect = start_text.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
    display_surface.blit(start_text, start_rect)

    quit_text = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 30).render("Press 'Q' to Quit", True, 'white')
    quit_rect = quit_text.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
    display_surface.blit(quit_text, quit_rect)

    pygame.display.update()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RETURN:
                    game_menu_music.stop()
                    main_game_loop()  # Start the game
                    waiting_for_input = False

def main_game_loop():
    # main game loop 
    game_over_music.stop()
    game_music.play(loops= -1)
    running = True
    while running:
        dt = clock.tick(60) / 1000
        # event loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == meteor_event:
                x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))
            
        all_sprites.update(dt)
        collisions()
        display_surface.fill('#3a2e3f')
        display_score()
        all_sprites.draw(display_surface)

        #test collision
        pygame.display.update()
        
    pygame.quit()

    
#general setup
pygame.init()
pygame.mixer.init()
# Set the dimensions of the canvas
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
#create canvas
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# set window captions
pygame.display.set_caption("Space Shooter v1.0")
running = True
score = 0
clock = pygame.time.Clock()

# import 
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()   
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)

laser_sounds = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sounds.set_volume(0.5)
damage_sounds = pygame.mixer.Sound(join('audio', 'damage.ogg'))
explosion_sounds = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sounds.set_volume(0.5)
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.8)
game_over_music = pygame.mixer.Sound(join('audio', 'game_over.mp3'))
game_menu_music = pygame.mixer.Sound(join('audio', 'game_menu.mp3'))

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):  # Add more stars if needed
    Star(all_sprites, star_surf)
player = Player(all_sprites, player_surf)

# create a custom event -> meteor event 
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

main_menu()

