import pygame
from config import WINDOW_WIDTH

def display_score(screen, font, score):
    text_surf = font.render(str(score), True, 'white')
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, 100))
    screen.blit(text_surf, text_rect)

    pygame.draw.rect(screen, 'white', text_rect.inflate(20,10).move(0,-8) , 5, 10)