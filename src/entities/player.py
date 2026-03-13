import pygame
from config import TILE_SIZE, COLOR_PLAYER, COLOR_BG

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, maze):
        nx = self.x + dx
        ny = self.y + dy
        if not maze.is_wall(nx, ny):
            self.x, self.y = nx, ny

    def draw(self, surface):
        p_rect = (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, COLOR_PLAYER, p_rect)
        pygame.draw.circle(surface, COLOR_BG, (self.x * TILE_SIZE + 10, self.y * TILE_SIZE + 10), 3)
        pygame.draw.circle(surface, COLOR_BG, (self.x * TILE_SIZE + 20, self.y * TILE_SIZE + 10), 3)