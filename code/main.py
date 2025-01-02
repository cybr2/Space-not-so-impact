import pygame
from game_manager import GameManager
from resources import load_resources
from config import WINDOW_WIDTH, WINDOW_HEIGHT

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()
    resources = load_resources()

    game_manager = GameManager(screen, clock, resources)
    game_manager.run()
    pygame.quit()

if __name__ == "__main__":
    main()
