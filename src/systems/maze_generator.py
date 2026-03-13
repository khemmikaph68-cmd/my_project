import random
from config import DIRS

class MazeGenerator:
    """สร้างเขาวงกตด้วยวิธี Recursive Backtracker + เจาะรูเพิ่มเพื่อลบล้างทางตัน"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self._generate()
        self._remove_dead_ends()

    def _generate(self):
        stack = [(1, 1)]
        self.grid[1][1] = 0

        while stack:
            cx, cy = stack[-1]
            neighbors = []

            for dx, dy in DIRS:
                nx, ny = cx + dx * 2, cy + dy * 2
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if self.grid[ny][nx] == 1:
                        neighbors.append((nx, ny, dx, dy))

            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                self.grid[cy + dy][cx + dx] = 0
                self.grid[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

    def _remove_dead_ends(self):
        """เจาะกำแพงบางส่วนออกเพื่อเชื่อมทาง"""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 0:
                    walls_around = 0
                    possible_drill = []

                    for dx, dy in DIRS:
                        if self.grid[y + dy][x + dx] == 1:
                            walls_around += 1
                            if 0 < x + dx * 2 < self.width - 1 and 0 < y + dy * 2 < self.height - 1:
                                if self.grid[y + dy * 2][x + dx * 2] == 0:
                                    possible_drill.append((dx, dy))

                    if walls_around >= 3 and possible_drill:
                        if random.random() < 0.6:  # โอกาส 60%
                            dx, dy = random.choice(possible_drill)
                            self.grid[y + dy][x + dx] = 0

    def is_wall(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] == 1