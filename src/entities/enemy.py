import pygame
from config import RED, ENEMY_SPEED_BASE
from .base import Entity

class Enemy(Entity):
    def __init__(self, x, y, level):
        super().__init__(x, y, 30, 30, RED)
        self.set_speed(ENEMY_SPEED_BASE + level - 1)  # Increase speed with level

    def update(self, player, maze):
        # Simple chase: move towards player
        dx = 0
        dy = 0
        if self.rect.centerx < player.rect.centerx:
            dx = self.get_speed()
        elif self.rect.centerx > player.rect.centerx:
            dx = -self.get_speed()
        if self.rect.centery < player.rect.centery:
            dy = self.get_speed()
        elif self.rect.centery > player.rect.centery:
            dy = -self.get_speed()
        
        # Try to move, if blocked, try only x or only y
        if dx != 0 or dy != 0:
            # Try full move
            old_x = self.rect.centerx
            old_y = self.rect.centery
            self.move(dx, dy, maze)
            if self.rect.centerx == old_x and self.rect.centery == old_y:
                # Blocked, try only x
                self.move(dx, 0, maze)
                if self.rect.centerx == old_x:
                    # Try only y
                    self.move(0, dy, maze)