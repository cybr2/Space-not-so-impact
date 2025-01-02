import pygame
from os.path import join

def load_resources():
    resources = {
        # images 
        "star": pygame.image.load(join('images', 'star.png')).convert_alpha(),
        "laser": pygame.image.load(join('images', 'laser.png')).convert_alpha(),
        "meteor": pygame.image.load(join('images', 'meteor.png')).convert_alpha(),
        "player": pygame.image.load(join('images', 'player.png')).convert_alpha(),
        "explosion": [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)],
        # text
        "font": join('images', 'Oxanium-Bold.ttf'),
        ""
        # sounds 
        "laser_sound": pygame.mixer.Sound(join('audio', 'laser.wav')),
        "explosion_sound": pygame.mixer.Sound(join('audio', 'explosion.wav')),
        "game_menu_music": pygame.mixer.Sound(join('audio', 'game_menu.mp3')),
        "game_music": pygame.mixer.Sound(join('audio', 'game_music.wav')),
        "game_over_music": pygame.mixer.Sound(join('audio', 'game_over.mp3'))
    }
    resources["laser_sound"].set_volume(0.5)
    resources["explosion_sound"].set_volume(0.5)
    resources["game_music"].set_volume(0.8)
    resources['game_menu_music'].set_volume(0.8)
    resources["game_over_music"].set_volume(0.8)
    return resources

