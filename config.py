import pygame

# --- Settings ---
TILE_SIZE = 30
MAZE_WIDTH = 25   # ควรเป็นเลขคี่
MAZE_HEIGHT = 21  # ควรเป็นเลขคี่
SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE
FPS = 60

# --- Colors ---
COLOR_WALL = (40, 40, 40)       # ผนังเขาวงกต (เทาเข้ม)
COLOR_PATH = (220, 220, 220)    # พื้นทางเดิน (ขาวหม่น)
COLOR_PLAYER = (0, 150, 255)    # ผู้เล่น (ฟ้า)
COLOR_ENEMY = (255, 0, 0)       # ปีศาจ (แดง)
COLOR_TROPHY = (255, 215, 0)    # ถ้วยรางวัล (ทอง)
COLOR_SKILL = (0, 255, 255)     # สกิลเวทมนตร์ (ฟ้าอ่อน)
COLOR_TEXT = (255, 255, 255)
COLOR_BG = (0, 0, 0)

# --- Directions ---
DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)] # บน, ล่าง, ซ้าย, ขวา