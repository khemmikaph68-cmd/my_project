import pygame
import random
from config import FPS, BLACK, WHITE, GREEN, RED, GRAY, CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT, LEVELS, COINS_PER_LEVEL, ENEMIES_PER_LEVEL_BASE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.coin import Coin
from src.systems.input_system import InputSystem

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.font = pygame.font.SysFont(None, 36)
        self.title_font = pygame.font.SysFont(None, 72)
        
        # Composition: นำระบบอื่นๆ เข้ามาประกอบร่างใน Game
        self.input_system = InputSystem()
        self.all_sprites = pygame.sprite.Group()
        
        self.level = 1
        self.coins_collected = 0
        self.game_state = "start"  # start, playing, level_complete, game_over
        
        # Preload level data so we can render quickly when starting
        self.load_level()

    def load_level(self):
        self.all_sprites.empty()
        self.maze = LEVELS[self.level - 1]
        self.player = None
        self.enemies = []
        self.coins = []
        
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                px = x * CELL_SIZE + CELL_SIZE // 2
                py = y * CELL_SIZE + CELL_SIZE // 2
                if cell == 'P':
                    self.player = Player(px, py)
                    self.all_sprites.add(self.player)
                elif cell == '.':
                    # Place coins randomly
                    if random.random() < 0.1 and len(self.coins) < COINS_PER_LEVEL:
                        coin = Coin(px, py)
                        self.coins.append(coin)
                        self.all_sprites.add(coin)
                    # Place enemies
                    elif random.random() < 0.05 and len(self.enemies) < ENEMIES_PER_LEVEL_BASE + self.level - 1:
                        enemy = Enemy(px, py, self.level)
                        self.enemies.append(enemy)
                        self.all_sprites.add(enemy)
        
        # Ensure we have exactly COINS_PER_LEVEL coins
        while len(self.coins) < COINS_PER_LEVEL:
            x = random.randint(1, MAZE_WIDTH - 2)
            y = random.randint(1, MAZE_HEIGHT - 2)
            if self.maze[y][x] == '.':
                px = x * CELL_SIZE + CELL_SIZE // 2
                py = y * CELL_SIZE + CELL_SIZE // 2
                coin = Coin(px, py)
                self.coins.append(coin)
                self.all_sprites.add(coin)
        
        # Ensure enemies
        while len(self.enemies) < ENEMIES_PER_LEVEL_BASE + self.level - 1:
            x = random.randint(1, MAZE_WIDTH - 2)
            y = random.randint(1, MAZE_HEIGHT - 2)
            if self.maze[y][x] == '.':
                px = x * CELL_SIZE + CELL_SIZE // 2
                py = y * CELL_SIZE + CELL_SIZE // 2
                enemy = Enemy(px, py, self.level)
                self.enemies.append(enemy)
                self.all_sprites.add(enemy)

    def update(self):
        # Start screen state (before the player begins the game)
        if self.game_state == "start":
            keys = self.input_system.get_keys()
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                self.level = 1
                self.coins_collected = 0
                self.game_state = "playing"
                self.load_level()
            return

        if self.game_state == "playing":
            # ดึง Input state ล่าสุด
            keys = self.input_system.get_keys()
            
            # อัปเดต Player โดยส่ง keys ไปด้วย (Dependency Injection อ่อนๆ)
            self.player.update(keys, self.maze)
            
            # อัปเดต Enemy
            for enemy in self.enemies:
                enemy.update(self.player, self.maze)
            
            # Check collisions
            for coin in self.coins[:]:
                if pygame.sprite.collide_rect(self.player, coin):
                    self.coins.remove(coin)
                    self.all_sprites.remove(coin)
                    self.coins_collected += 1
            
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(self.player, enemy):
                    self.game_state = "game_over"
            
            if self.coins_collected >= COINS_PER_LEVEL:
                self.game_state = "level_complete"
        
        elif self.game_state == "level_complete":
            keys = self.input_system.get_keys()
            if keys[pygame.K_SPACE]:
                self.level += 1
                if self.level > len(LEVELS):
                    self.level = 1  # Loop back
                self.coins_collected = 0
                self.game_state = "playing"
                self.load_level()
        
        elif self.game_state == "game_over":
            keys = self.input_system.get_keys()
            if keys[pygame.K_r]:
                self.level = 1
                self.coins_collected = 0
                self.game_state = "playing"
                self.load_level()

    def draw(self):
        self.screen.fill(BLACK)

        # When the game is being played (or ended/complete), draw the maze + sprites.
        if self.game_state in ("playing", "level_complete", "game_over"):
            for y, row in enumerate(self.maze):
                for x, cell in enumerate(row):
                    if cell == '#':
                        pygame.draw.rect(self.screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            self.all_sprites.draw(self.screen)

            # Draw UI
            text = self.font.render(f"Level: {self.level} Coins: {self.coins_collected}/{COINS_PER_LEVEL}", True, WHITE)
            self.screen.blit(text, (10, 10))

            if self.game_state == "level_complete":
                text = self.font.render("Level Complete! Press SPACE for next level", True, GREEN)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            elif self.game_state == "game_over":
                text = self.font.render("Game Over! Press R to restart", True, RED)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        elif self.game_state == "start":
            title = self.title_font.render("Maze of Terror", True, WHITE)
            subtitle = self.font.render("Press ENTER to start", True, WHITE)
            controls = self.font.render("Use arrow keys to move, collect coins, avoid enemies", True, GRAY)

            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.is_running = self.input_system.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)