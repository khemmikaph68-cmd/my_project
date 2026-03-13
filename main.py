import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE
from src.game import Game

def main():
    print("Starting game...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Initialization
    game = Game(screen)
    print("Game initialized, starting run...")
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()