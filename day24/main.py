from collections import defaultdict
from dataclasses import dataclass
from itertools import count


dirs = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1),
}
all_moves = set(dirs.values()) | {(0, 0)}


@dataclass
class Blizzard:
    x: int
    y: int
    dx: int
    dy: int

    def move(self, w, h):
        self.x += self.dx
        self.y += self.dy

        if self.x < 1:
            self.x += w - 2
        if self.y < 1:
            self.y += h - 2
        if self.x > w - 2:
            self.x -= w - 2
        if self.y > h - 2:
            self.y -= h - 2


def move_to_goal(grid, bliz, x, y):
    w, h = len(grid[0]), len(grid)
    goal_y = len(grid) - 1 if y == 0 else 0
    future = defaultdict(set)
    world = defaultdict(int)
    future[0].add((x, y))
    for time in count():
        world.clear()
        for b in bliz:
            world[(b.x, b.y)] += 1
            b.move(w, h)
        for x, y in future.pop(time):
            if world[(x, y)] != 0:
                continue
            if y == goal_y:
                return time, x, y
            for dx, dy in all_moves:
                nx, ny = x + dx, y + dy
                in_bounds = ny >= 0 and ny < h
                if ny >= 0 and ny < h and grid[ny][nx] == '.':
                    future[time + 1].add((nx, ny))


def solve(lines, times=1):
    grid = []
    bliz = []
    x = None
    y = 0
    for line in lines:
        line = list(line)
        if x is None:
            x = line.index('.')
        for i, c in enumerate(line):
            if c in dirs:
                bliz.append(Blizzard(i, len(grid), *dirs[c]))
                line[i] = '.'
        grid.append(line)

    total = 0
    for _ in range(int(times)):
        subtotal, x, y = move_to_goal(grid, bliz, x, y)
        total += subtotal + 1
    return total - 1
