import pygame
from config import TILE_SIZE, COLOR_PLAYER, COLOR_BG
from src.entities.base import Entity # นำเข้าคลาสแม่

class Player(Entity): # <--- Inheritance (สืบทอดคุณสมบัติจาก Entity)
    def __init__(self, x, y):
        super().__init__(x, y) # เรียกใช้ __init__ ของคลาสแม่
        self.is_ghost = False
        self.ghost_timer = 0.0

    def move(self, dx, dy, maze):
        nx = self.x + dx
        ny = self.y + dy
        if self.is_ghost or not maze.is_wall(nx, ny):
            self.x, self.y = nx, ny

    # ---> Polymorphism (เขียนทับ Method ของคลาสแม่) <---
    def update(self, dt):
        if self.is_ghost:
            self.ghost_timer -= dt
            if self.ghost_timer <= 0:
                self.is_ghost = False
                self.ghost_timer = 0.0

    # ---> Polymorphism (เขียนทับ Method ของคลาสแม่) <---
    def draw(self, surface):
        color = (180, 100, 255) if self.is_ghost else COLOR_PLAYER
        p_rect = (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, color, p_rect)
        
        eye_color = (255, 255, 255) if self.is_ghost else COLOR_BG
        pygame.draw.circle(surface, eye_color, (self.x * TILE_SIZE + 10, self.y * TILE_SIZE + 10), 3)
        pygame.draw.circle(surface, eye_color, (self.x * TILE_SIZE + 20, self.y * TILE_SIZE + 10), 3)