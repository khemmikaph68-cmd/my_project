import pygame
from config import GREEN, PLAYER_SPEED
from .base import Entity

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, GREEN)
        self.set_speed(PLAYER_SPEED)

    def update(self, keys, maze):
        # Polymorphism: การทำงานของ update เปลี่ยนแปลงไปเป็นของ Player
        speed = self.get_speed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx = -speed
        if keys[pygame.K_RIGHT]:
            dx = speed
        if keys[pygame.K_UP]:
            dy = -speed
        if keys[pygame.K_DOWN]:
            dy = speed
        if dx != 0 or dy != 0:
            self.move(dx, dy, maze)