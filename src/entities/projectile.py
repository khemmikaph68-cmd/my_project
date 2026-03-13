import pygame
from config import TILE_SIZE, COLOR_SKILL

class MagicProjectile:
    """กระสุนสกิลเวทมนตร์ ปาเพื่อ Slow ปีศาจ"""
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = float(start_x * TILE_SIZE + TILE_SIZE // 2)
        self.y = float(start_y * TILE_SIZE + TILE_SIZE // 2)
        
        dx = (target_x * TILE_SIZE + TILE_SIZE // 2) - self.x
        dy = (target_y * TILE_SIZE + TILE_SIZE // 2) - self.y
        length = (dx**2 + dy**2)**0.5
        
        if length > 0:
            self.vx = (dx / length) * 600.0 
            self.vy = (dy / length) * 600.0
        else:
            self.vx, self.vy = 0, 0
            
        self.radius = 8
        self.active = True

    def update(self, dt, maze):
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        grid_x = int(self.x // TILE_SIZE)
        grid_y = int(self.y // TILE_SIZE)
        if maze.is_wall(grid_x, grid_y):
            self.active = False
            
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, COLOR_SKILL, (int(self.x), int(self.y)), self.radius)