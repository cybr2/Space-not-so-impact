import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from random import randint
from entities.player import Player
from entities.meteor import Meteor
from entities.star import Star
from utils.collisions import collision
from utils.display_score import display_score
from entities.enemy import Enemy


class GameManager:
    def __init__(self, screen, clock, resources):
        self.screen = screen
        self.clock = clock
        self.resources = resources
        self.running = True
        self.state = "menu"
        self.title_font = pygame.font.Font(self.resources["font"], 60)
        self.subtitle_font = pygame.font.Font(self.resources["font"], 40)
        self.all_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.score = 0
        self.dt = self.clock.tick(60) / 1000

        #create stars
        for _ in range(20):
            Star(self.all_sprites, self.resources)
        
        self.player = Player(self.all_sprites, self.resources, self.all_sprites, self.laser_sprites)

        #create meteor spawn event
        self.meteor_event = pygame.event.custom_type()
        pygame.time.set_timer(self.meteor_event, 500)

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 3000) 
    
    def reset_game(self):
        # Reset the score
        self.score = 0

        # Reset the player's position
        self.player.rect.midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 10)

        self.player.rect.midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT / 2 - 50)

        # Reset any other player properties (e.g., health, if applicable)
        # Example: self.player.health = self.player.max_health

        # Clear all sprite groups
        self.all_sprites.empty()
        self.meteor_sprites.empty()
        self.laser_sprites.empty()
        self.enemy_sprites.empty()

        # Recreate the stars and other entities
        for _ in range(20):
            Star(self.all_sprites, self.resources)

        # Recreate the player
        self.player = Player(self.all_sprites, self.resources, self.all_sprites, self.laser_sprites)

        # Reset the meteor spawn timer
        pygame.time.set_timer(self.meteor_event, 500)
        # Reset the enemy spawn timer
        # pygame.time.set_timer(self.enemy_event, 500)

        # Optionally, reset other game logic (like power-ups, level, etc.)

        
    def run(self):
        while self.running:
            # self.dt = self.clock.tick(60) / 1000
            if self.state == "menu":
                self.show_main_menu()
            elif self.state == "playing":
                self.play_game()
            elif self.state == "game_over":
                self.show_game_over()

    def show_main_menu(self):
        self.resources["game_menu_music"].play(loops=-1)
        menu_active = True
        while menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    menu_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start game
                        self.state = "playing"
                        menu_active = False
                    elif event.key == pygame.K_ESCAPE:  # Quit game
                        self.running = False
                        menu_active = False

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Render title
            text_surf = self.title_font.render("Space Not So Impact", True, 'white')
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
            self.screen.blit(text_surf, text_rect)

            # Render "Start" option
            start_text = self.subtitle_font.render("Press 'Enter' to Start", True, 'white')
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
            self.screen.blit(start_text, start_rect)

            # Render "Quit" option
            quit_text = self.subtitle_font.render("Press 'Esc' to Exit", True, 'white')
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
            self.screen.blit(quit_text, quit_rect)

            # Update the display
            pygame.display.update()
            self.clock.tick(60)

        self.resources["game_menu_music"].stop()

    def play_game(self):
        self.reset_game()
        start_time = pygame.time.get_ticks() 
        self.resources["game_music"].play(loops= -1)
        game_active = True
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        game_active = False
                        # self.resources["game_music"].stop()
                        # self.show_main_menu()
                elif event.type == self.meteor_event:
                    x,y = randint(0, WINDOW_WIDTH), randint(-200, -100)
                    Meteor(self.resources, (x,y), (self.all_sprites, self.meteor_sprites))
                elif event.type == self.enemy_event:
                    # Randomize spawn position
                    x,y = randint(0, WINDOW_WIDTH - 20), randint(-100, 10)  # Ensure enemy stays within screen bounds
                    Enemy(self.resources,self.all_sprites, (x,y),self.laser_sprites, (self.all_sprites , self.enemy_sprites))

            self.score = (pygame.time.get_ticks() - start_time) // 1000

            # Clear the screen
            self.screen.fill('#3a2e3f')
            self.all_sprites.update(self.dt)
             # Check collisions
            game_active = collision(
                self.resources, 
                self.player, 
                self.meteor_sprites, 
                self.laser_sprites, 
                self.all_sprites, 
                self.enemy_sprites,
                game_active,
            )

            # Handle state transition on game over
            if not game_active:
                self.resources["game_music"].stop()
                if self.state == "menu":
                    break
                else:
                    self.state = "game_over"
                    break
            
            display_score(self.screen, self.subtitle_font, self.score)
            
            self.all_sprites.draw(self.screen)
            pygame.display.update()
            self.dt = self.clock.tick(60) / 1000

    def show_game_over(self):
        self.resources["game_over_music"].play(loops=-1)
        game_over_active = True
        while game_over_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    game_over_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Start game
                        self.state = "playing"
                        game_over_active = False
                    elif event.key == pygame.K_q:  # Quit game
                        game_over_active = False
                        self.state = "menu"

            # Clear the screen
            self.screen.fill('#3a2e3f')

            # Render title
            text_surf = self.title_font.render("Game Over", True, 'white')
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
            self.screen.blit(text_surf, text_rect)

            # Render "Score"
            score_surf = self.subtitle_font.render(f"Score: {self.score}", True, 'white')
            score_rect = score_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
            self.screen.blit(score_surf, score_rect)

            # Render "Restart" option
            restart_text = self.subtitle_font.render("Press 'R' to Restart or 'Q' to Quit", True, 'white')
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
            self.screen.blit(restart_text, restart_rect)

            # Handle state transition on game over
            if not game_over_active:
                self.resources["game_over_music"].stop()
                break

            # Update the display
            pygame.display.update()
            self.clock.tick(60)



        self.resources["game_menu_music"].stop()
