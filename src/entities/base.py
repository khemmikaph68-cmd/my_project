import pygame
from config import CELL_SIZE

class Entity(pygame.sprite.Sprite):
    """Base class สำหรับทุกวัตถุในเกม (Open/Closed Principle - ขยายได้โดยไม่ต้องแก้คลาสนี้)"""
    
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Encapsulation: ซ่อนตัวแปร speed ไว้ใช้งานภายใน
        self._speed = 0 
        self.grid_x = x // CELL_SIZE
        self.grid_y = y // CELL_SIZE

    # Encapsulation: ใช้ Getter/Setter ในการเข้าถึงข้อมูล
    def set_speed(self, speed):
        if speed >= 0:
            self._speed = speed
            
    def get_speed(self):
        return self._speed

    def update(self, *args, **kwargs):
        """Method ที่รอให้ Subclass นำไปเขียนทับ (Polymorphism)"""
        pass

    def move(self, dx, dy, maze):
        """Move entity by dx, dy, checking maze walls"""
        new_x = self.rect.centerx + dx
        new_y = self.rect.centery + dy
        grid_x = new_x // CELL_SIZE
        grid_y = new_y // CELL_SIZE
        if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze) and maze[grid_y][grid_x] != '#':
            self.rect.centerx = new_x
            self.rect.centery = new_y
            self.grid_x = grid_x
            self.grid_y = grid_y