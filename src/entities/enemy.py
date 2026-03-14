import pygame
import heapq
import random
from config import TILE_SIZE, COLOR_ENEMY, COLOR_BG, DIRS
from src.entities.base import Entity # นำเข้าคลาสแม่

class Enemy(Entity):
    def __init__(self, x, y, maze, ai_type="A*"):
        super().__init__(x, y)
        self.maze = maze
        self.ai_type = ai_type
        self.path = []
        self.base_delay = 0.25
        self.timer = 0.0
        
        # เพิ่มตัวแปรสำหรับจำ "ตำแหน่งล่าสุด" เพื่อป้องกันการเดินถอยหลังกลับไปกลับมา
        self.last_x = x
        self.last_y = y

    def draw(self, surface):
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
            if current == goal: break
            for dx, dy in DIRS:
                nx, ny = current[0] + dx, current[1] + dy
                if nx < 0 or nx >= self.maze.width or ny < 0 or ny >= self.maze.height: continue
                if self.maze.is_wall(nx, ny): continue
                next_node = (nx, ny)
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        current = goal
        path = []
        if current not in came_from: return [] 
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def get_random_move(self):
        valid_moves = []
        for dx, dy in DIRS:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                if not self.maze.is_wall(nx, ny):
                    valid_moves.append((nx, ny))
                    
        # กรองเอาช่องที่เรา "เพิ่งเดินจากมา" ออกไป เพื่อไม่ให้มันเดินย้อนกลับ
        forward_moves = [pos for pos in valid_moves if pos != (self.last_x, self.last_y)]

        # ถ้ามีทางไปต่อ ให้สุ่มจากทางที่ไม่ใช่ทางเดิม
        if forward_moves: 
            chosen = random.choice(forward_moves)
        # แต่ถ้าไม่มีทางเลือกอื่นแล้ว (คือเจอทางตัน) ก็ต้องยอมเดินถอยหลังกลับไปทางเดิม
        elif valid_moves: 
            chosen = valid_moves[0]
        else:
            chosen = (self.x, self.y)

        # อัปเดตตำแหน่งปัจจุบันให้กลายเป็น "อดีต" สำหรับรอบถัดไป
        self.last_x, self.last_y = self.x, self.y
        return chosen

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