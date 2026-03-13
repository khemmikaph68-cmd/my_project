import pygame
import random
import sys
from config import *
from src.systems.maze_generator import MazeGenerator
from src.entities.player import Player
from src.entities.enemy import AStarEnemy
from src.entities.projectile import MagicProjectile

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # เพิ่มฟอนต์สำหรับหน้า Title โดยเฉพาะให้ใหญ่และหนาขึ้น
        self.title_font = pygame.font.SysFont('Tahoma', 64, bold=True)
        self.font = pygame.font.SysFont('Tahoma', 36)
        self.small_font = pygame.font.SysFont('Tahoma', 20)
        self.running = True
        
        self.reset_game()
        
        # บังคับให้เริ่มเปิดเกมมาอยู่ที่หน้า START
        self.state = "START" 

    def reset_game(self):
        self.maze = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        self.player = Player(1, 1)
        
        self.trophy_x = MAZE_WIDTH - 2
        self.trophy_y = MAZE_HEIGHT - 2
        self.maze.grid[self.trophy_y][self.trophy_x] = 0
        self.maze.grid[self.trophy_y-1][self.trophy_x] = 0
        self.maze.grid[self.trophy_y][self.trophy_x-1] = 0

        ex, ey = MAZE_WIDTH // 2, MAZE_HEIGHT // 2
        while self.maze.is_wall(ex, ey) or (ex <= 8 and ey <= 8):
            ex = random.randint(MAZE_WIDTH // 2, MAZE_WIDTH - 2)
            ey = random.randint(MAZE_HEIGHT // 2, MAZE_HEIGHT - 2)
            
        self.enemy = AStarEnemy(ex, ey, self.maze)
        self.projectiles = []
        
        self.skill_cooldown = 5.0 
        self.current_cooldown = 0.0
        self.state = "PLAYING"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # ถ้าอยู่หน้า START ให้กด SPACE หรือ ENTER เพื่อเริ่มเกม
                if self.state == "START":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset_game()
                
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
                        self.reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "PLAYING" and event.button == 1: 
                    if self.current_cooldown <= 0:
                        mx, my = pygame.mouse.get_pos()
                        target_grid_x = mx // TILE_SIZE
                        target_grid_y = my // TILE_SIZE
                        self.projectiles.append(MagicProjectile(self.player.x, self.player.y, target_grid_x, target_grid_y))
                        self.current_cooldown = self.skill_cooldown

    def update_logic(self, dt):
        if self.state == "PLAYING":
            if self.current_cooldown > 0:
                self.current_cooldown -= dt

            self.enemy.update(dt, self.player.x, self.player.y)

            enemy_rect = pygame.Rect(self.enemy.x * TILE_SIZE, self.enemy.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            for p in self.projectiles:
                p.update(dt, self.maze)
                if p.active and p.get_rect().colliderect(enemy_rect):
                    p.active = False
                    self.enemy.apply_slow(4.0)

            self.projectiles = [p for p in self.projectiles if p.active]

            if self.player.x == self.trophy_x and self.player.y == self.trophy_y:
                self.state = "WIN"
            if self.player.x == self.enemy.x and self.player.y == self.enemy.y:
                self.state = "LOSE"

    def draw(self):
        self.screen.fill(COLOR_WALL)
        
        # --- วาดหน้าจอ START ---
        if self.state == "START":
            # ตกแต่งพื้นหลังนิดหน่อยให้ดูเป็นตาราง (Grid)
            for x in range(0, SCREEN_WIDTH, TILE_SIZE * 2):
                pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE * 2):
                pygame.draw.line(self.screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))

            # ชื่อเกม
            title = self.title_font.render("MAZE OF TERROR", True, COLOR_ENEMY)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
            self.screen.blit(title, title_rect)
            
            # คำอธิบาย
            desc = self.small_font.render("Find the trophy. Avoid the red monster. Click to cast Slow Magic.", True, COLOR_PATH)
            desc_rect = desc.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(desc, desc_rect)

            # ตัวหนังสือกระพริบ "Press SPACE to Start"
            if pygame.time.get_ticks() % 1000 < 500:  # กระพริบทุกๆ 0.5 วินาที
                blink_text = self.font.render("Press SPACE to Start", True, COLOR_TROPHY)
                blink_rect = blink_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
                self.screen.blit(blink_text, blink_rect)

        # --- วาดหน้าจอตอนเล่น และจบเกม ---
        else:
            for y in range(MAZE_HEIGHT):
                for x in range(MAZE_WIDTH):
                    if self.maze.grid[y][x] == 0:
                        rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(self.screen, COLOR_PATH, rect)

            center = (self.trophy_x * TILE_SIZE + TILE_SIZE//2, self.trophy_y * TILE_SIZE + TILE_SIZE//2)
            pygame.draw.circle(self.screen, COLOR_TROPHY, center, TILE_SIZE//3)
            
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            for p in self.projectiles:
                p.draw(self.screen)

            cd_ratio = max(0, 1 - (self.current_cooldown / self.skill_cooldown))
            pygame.draw.rect(self.screen, (100, 100, 100), (10, 10, 150, 15))
            pygame.draw.rect(self.screen, COLOR_SKILL, (10, 10, int(150 * cd_ratio), 15))
            text = self.small_font.render("Skill", True, COLOR_TEXT)
            self.screen.blit(text, (10, 30))

            if self.state in ["WIN", "LOSE"]:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(COLOR_BG)
                self.screen.blit(overlay, (0, 0))

                msg = "YOU ESCAPED! (Win!)" if self.state == "WIN" else "WASTED! (Game Over)"
                color = COLOR_TROPHY if self.state == "WIN" else COLOR_ENEMY
                
                text = self.font.render(msg, True, color)
                rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
                self.screen.blit(text, rect)

                btn = self.small_font.render("Press 'R' to play again", True, COLOR_TEXT)
                b_rect = btn.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
                self.screen.blit(btn, b_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update_logic(dt)
            self.draw()