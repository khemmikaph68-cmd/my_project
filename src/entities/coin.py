import pygame
from config import YELLOW
from .base import Entity

class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, YELLOW)