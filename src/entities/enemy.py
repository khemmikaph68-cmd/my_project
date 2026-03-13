import pygame
import heapq
import random
from config import TILE_SIZE, COLOR_ENEMY, COLOR_BG, DIRS

class Enemy:
    def __init__(self, x, y, maze, ai_type="A*"):
        self.x = x
        self.y = y
        self.maze = maze
        self.ai_type = ai_type
        self.path = []
        
        self.base_delay = 0.25
        self.timer = 0.0

    def draw(self, surface):
        # ตัวล่า (A*) สีแดง, ตัวเฝ้าด่านเดินสุ่ม (Random) สีส้ม
        color = COLOR_ENEMY if self.ai_type == "A*" else (255, 140, 0)
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, color, rect)
        
        pygame.draw.circle(surface, COLOR_BG, (self.x * TILE_SIZE + 8, self.y * TILE_SIZE + 10), 3)
        pygame.draw.circle(surface, COLOR_BG, (self.x * TILE_SIZE + 22, self.y * TILE_SIZE + 10), 3)
        pygame.draw.line(surface, COLOR_BG, (self.x * TILE_SIZE + 10, self.y * TILE_SIZE + 22), (self.x * TILE_SIZE + 20, self.y * TILE_SIZE + 22), 3)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, target_x, target_y):
        start = (self.x, self.y)
        goal = (target_x, target_y)

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]
            if current == goal:
                break

            for dx, dy in DIRS:
                nx, ny = current[0] + dx, current[1] + dy
                # ป้องกัน A* เดินทะลุวาร์ปหรือนอกจอ
                if nx < 0 or nx >= self.maze.width or ny < 0 or ny >= self.maze.height:
                    continue
                if self.maze.is_wall(nx, ny):
                    continue
                    
                next_node = (nx, ny)
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        current = goal
        path = []
        if current not in came_from:
            return [] 

        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def get_random_move(self):
        valid_moves = []
        for dx, dy in DIRS:
            nx, ny = self.x + dx, self.y + dy
            # ห้าม Random เดินทะลุขอบจอ
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                if not self.maze.is_wall(nx, ny):
                    valid_moves.append((nx, ny))
        
        if valid_moves:
            return random.choice(valid_moves)
        return self.x, self.y

    def update(self, dt, target_x, target_y):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.base_delay
            if self.ai_type == "A*":
                self.path = self.find_path(target_x, target_y)
                if self.path:
                    self.x, self.y = self.path[0]
            else:
                self.x, self.y = self.get_random_move()