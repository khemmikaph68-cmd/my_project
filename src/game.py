import pygame
import random
import sys
from config import *
from src.systems.maze_generator import MazeGenerator
from src.entities.player import Player
from src.entities.enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        self.title_font = pygame.font.SysFont('Tahoma', 64, bold=True)
        self.font = pygame.font.SysFont('Tahoma', 36)
        self.small_font = pygame.font.SysFont('Tahoma', 20)
        self.running = True
        
        self.level = 1
        self.start_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50)
        self.state = "START"
        self.reset_game()
        self.state = "START"

    def get_random_empty_cell(self):
        while True:
            x = random.randint(1, MAZE_WIDTH - 2)
            y = random.randint(1, MAZE_HEIGHT - 2)
            # ป้องกันไม่ให้เหรียญ/ไอเทม/ปีศาจ ไปเกิดทับบนประตูมิติ
            invalid_pos = [self.portal_1, self.portal_2]
            if not self.maze.is_wall(x, y) and (x, y) not in invalid_pos:
                return x, y

    def reset_game(self, reset_level=False):
        if reset_level:
            self.level = 1
            
        self.maze = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        self.player = Player(1, 1)
        
        # ตั้งค่าตำแหน่งประตูมิติ (มุมซ้ายบน และ ขวาล่าง)
        self.portal_1 = (1, 1)
        self.portal_2 = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
        # ให้ cooldown เริ่มต้นที่ 1 วินาที เพื่อกันไม่ให้เริ่มเกมปุ๊บวาร์ปปั๊บ
        self.teleport_cooldown = 1.0 
        
        self.coins = []
        for _ in range(3):
            cx, cy = self.get_random_empty_cell()
            while (cx, cy) in self.coins:
                cx, cy = self.get_random_empty_cell()
            self.coins.append((cx, cy))

        self.ghost_item = None
        if self.level >= 3:
            gx, gy = self.get_random_empty_cell()
            while (gx, gy) in self.coins:
                gx, gy = self.get_random_empty_cell()
            self.ghost_item = (gx, gy)

        self.enemies = []
        num_astar = 0
        num_random = 0
        
        if self.level in [1, 2]:
            num_astar, num_random = 1, 0
        elif self.level in [3, 4]:
            num_astar, num_random = 1, 1
        elif self.level in [5, 6]:
            num_astar, num_random = 2, 1
        else:
            num_astar, num_random = 2, 2
            
        ai_list = ["A*"] * num_astar + ["RANDOM"] * num_random
        new_delay = max(0.15, 0.4 - (self.level * 0.02))

        for ai in ai_list:
            ex, ey = self.get_random_empty_cell()
            while ex <= 10 and ey <= 10:
                ex, ey = self.get_random_empty_cell()
                
            enemy = Enemy(ex, ey, self.maze, ai_type=ai)
            enemy.base_delay = new_delay
            enemy.timer = new_delay
            self.enemies.append(enemy)
            
        self.state = "PLAYING"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "START":
                    if event.button == 1 and self.start_btn_rect.collidepoint(event.pos):
                        self.reset_game(reset_level=False)

            if event.type == pygame.KEYDOWN:
                if self.state == "START":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset_game(reset_level=False)
                
                elif self.state == "PLAYING":
                    dx, dy = 0, 0
                    if event.key in (pygame.K_LEFT, pygame.K_a): dx = -1
                    elif event.key in (pygame.K_RIGHT, pygame.K_d): dx = 1
                    elif event.key in (pygame.K_UP, pygame.K_w): dy = -1
                    elif event.key in (pygame.K_DOWN, pygame.K_s): dy = 1
                    
                    if dx != 0 or dy != 0:
                        self.player.move(dx, dy, self.maze)
                        
                elif self.state in ["WIN", "LOSE"]:
                    if event.key == pygame.K_r:
                        if self.state == "LOSE":
                            self.reset_game(reset_level=False)
                            self.state = "START"
                        else:
                            self.level += 1
                            self.reset_game(reset_level=False)

    def update_logic(self, dt):
        if self.state == "PLAYING":
            self.player.update(dt)

            if not self.player.is_ghost and self.maze.is_wall(self.player.x, self.player.y):
                self.state = "LOSE"
                return

            # --- ระบบวาร์ปด้วยประตูมิติ ---
            if self.teleport_cooldown > 0:
                self.teleport_cooldown -= dt
            else:
                if (self.player.x, self.player.y) == self.portal_1:
                    self.player.x, self.player.y = self.portal_2
                    self.teleport_cooldown = 1.0 # หน่วงเวลา 1 วิกันวาร์ปกลับไปกลับมารัวๆ
                elif (self.player.x, self.player.y) == self.portal_2:
                    self.player.x, self.player.y = self.portal_1
                    self.teleport_cooldown = 1.0

            for enemy in self.enemies:
                enemy.update(dt, self.player.x, self.player.y)
                if self.player.x == enemy.x and self.player.y == enemy.y:
                    self.state = "LOSE"

            if (self.player.x, self.player.y) in self.coins:
                self.coins.remove((self.player.x, self.player.y))
                
            if self.ghost_item and (self.player.x, self.player.y) == self.ghost_item:
                self.player.is_ghost = True
                self.player.ghost_timer = 4.0
                self.ghost_item = None
            
            if len(self.coins) == 0:
                self.state = "WIN"

    def draw(self):
        self.screen.fill(COLOR_WALL)
        
        if self.state == "START":
            for x in range(0, SCREEN_WIDTH, TILE_SIZE * 2):
                pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE * 2):
                pygame.draw.line(self.screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))

            title = self.title_font.render("MAZE OF TERROR", True, COLOR_ENEMY)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3 - 30))
            self.screen.blit(title, title_rect)
            
            level_text = self.font.render(f"Current Level: {self.level}", True, COLOR_TROPHY)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 40))
            self.screen.blit(level_text, level_rect)

            pygame.draw.rect(self.screen, COLOR_PLAYER, self.start_btn_rect, border_radius=10)
            start_text = self.font.render("START", True, COLOR_TEXT)
            start_text_rect = start_text.get_rect(center=self.start_btn_rect.center)
            self.screen.blit(start_text, start_text_rect)

            desc = self.small_font.render("Collect 3 coins. Use portals. Lvl 3+ has Ghost Orb.", True, COLOR_PATH)
            desc_rect = desc.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
            self.screen.blit(desc, desc_rect)

        else:
            for y in range(MAZE_HEIGHT):
                for x in range(MAZE_WIDTH):
                    if self.maze.grid[y][x] == 0:
                        rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(self.screen, COLOR_PATH, rect)

            # วาดประตูมิติ (วาดก่อนตัวละครเพื่อให้อยู่ที่พื้น)
            for px, py in [self.portal_1, self.portal_2]:
                center = (px * TILE_SIZE + TILE_SIZE//2, py * TILE_SIZE + TILE_SIZE//2)
                # วงนอกสีฟ้าเข้ม
                pygame.draw.circle(self.screen, (0, 100, 255), center, TILE_SIZE//2 - 2)
                # วงในสีฟ้าสว่างให้ดูเรืองแสง
                pygame.draw.circle(self.screen, (150, 255, 255), center, TILE_SIZE//4)

            for cx, cy in self.coins:
                center = (cx * TILE_SIZE + TILE_SIZE//2, cy * TILE_SIZE + TILE_SIZE//2)
                pygame.draw.circle(self.screen, COLOR_TROPHY, center, TILE_SIZE//3)
                
            if self.ghost_item:
                gx, gy = self.ghost_item
                center = (gx * TILE_SIZE + TILE_SIZE//2, gy * TILE_SIZE + TILE_SIZE//2)
                pygame.draw.circle(self.screen, (0, 255, 255), center, TILE_SIZE//4) # ใช้สีฟ้าเขียวแทน
            
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)

            ui_text = self.small_font.render(f"Level: {self.level} | Coins: {3 - len(self.coins)}/3", True, COLOR_BG)
            self.screen.blit(ui_text, (10, 10))
            
            if self.player.is_ghost:
                ghost_txt = self.small_font.render(f"GHOST: {self.player.ghost_timer:.1f}s", True, (0, 255, 255))
                self.screen.blit(ghost_txt, (SCREEN_WIDTH - 150, 10))

            if self.state in ["WIN", "LOSE"]:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(COLOR_BG)
                self.screen.blit(overlay, (0, 0))

                if self.state == "WIN":
                    msg = f"LEVEL {self.level} CLEARED!"
                    color = COLOR_TROPHY
                    btn_msg = "Press 'R' for Next Level"
                else:
                    msg = "WASTED! (Game Over)"
                    color = COLOR_ENEMY
                    btn_msg = f"Press 'R' to retry Level {self.level}"
                
                text = self.font.render(msg, True, color)
                rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
                self.screen.blit(text, rect)

                btn = self.small_font.render(btn_msg, True, COLOR_TEXT)
                b_rect = btn.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
                self.screen.blit(btn, b_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update_logic(dt)
            self.draw()