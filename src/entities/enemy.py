import pygame
import heapq
from config import TILE_SIZE, COLOR_ENEMY, COLOR_SKILL, COLOR_BG, DIRS

class AStarEnemy:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.path = []
        
        self.base_delay = 0.25 # วินาที (วิ่งเร็วกว่าคนปกติหน่อย)
        self.current_delay = self.base_delay
        self.slow_timer = 0.0
        self.is_slowed = False
        self.timer = 0.0

    def apply_slow(self, duration_sec):
        self.is_slowed = True
        self.slow_timer = duration_sec
        self.current_delay = 0.7 

    def draw(self, surface):
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, COLOR_ENEMY, rect)
        
        eye_color = COLOR_SKILL if self.is_slowed else COLOR_BG
        pygame.draw.circle(surface, eye_color, (self.x * TILE_SIZE + 8, self.y * TILE_SIZE + 10), 3)
        pygame.draw.circle(surface, eye_color, (self.x * TILE_SIZE + 22, self.y * TILE_SIZE + 10), 3)
        pygame.draw.line(surface, eye_color, (self.x * TILE_SIZE + 10, self.y * TILE_SIZE + 22), (self.x * TILE_SIZE + 20, self.y * TILE_SIZE + 22), 3)

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
                next_node = (current[0] + dx, current[1] + dy)
                if self.maze.is_wall(next_node[0], next_node[1]):
                    continue
                    
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

    def update(self, dt, target_x, target_y):
        if self.is_slowed:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.is_slowed = False
                self.current_delay = self.base_delay

        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.current_delay
            self.path = self.find_path(target_x, target_y)
            if self.path:
                next_step = self.path[0]
                self.x, self.y = next_step