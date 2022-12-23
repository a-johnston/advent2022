from collections import defaultdict
from itertools import count


moves = (
    (0, -1), (1, -1), (-1, -1),
    (0, 1), (1, 1), (-1, 1),
    (-1, 0), (-1, -1), (-1, 1),
    (1, 0), (1, -1), (1, 1),
)
adjacent = set(moves)


class Elf:
    def __init__(self, idx, x, y):
        self.idx = idx
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.moves = list(moves)

    def count(self, grid, m):
        count = 0
        for dx, dy in m:
            if grid[(self.x + dx, self.y + dy)] >> 8 > 0:
                count += 1
        return count

    def setup(self, grid):
        grid[(self.x, self.y)] = self.idx << 8

    def mark(self, grid):
        self.last_x = self.x
        self.last_y = self.y
        if self.count(grid, adjacent) > 0:
            for i in range(0, len(moves), 3):
                if self.count(grid, self.moves[i:i+3]) == 0:
                    self.x += self.moves[i][0]
                    self.y += self.moves[i][1]
                    break
        self.moves = self.moves[3:] + self.moves[:3]
        grid[(self.x, self.y)] += 1

    def check(self, grid):
        if grid[(self.x, self.y)] & 255 != 1:
            self.x = self.last_x
            self.y = self.last_y

    def moved(self):
        return self.x != self.last_x or self.y != self.last_y


def solve(lines, rounds=10):
    elves = []
    y = 0
    for line in lines:
        x = -1
        while (x := line.find('#', x + 1)) != -1:
            elves.append(Elf(len(elves) + 1, x, y))
        y += 1

    grid = defaultdict(int)
    if int(rounds) > 0:
        it = range(int(rounds))
    else:
        it = count(1)
    for idx in it:
        grid.clear()
        for elf in elves:
            elf.setup(grid)
        for elf in elves:
            elf.mark(grid)
        for elf in elves:
            elf.check(grid)
        for elf in elves:
            if elf.moved():
                break
        else:
            return idx

    xs = [elf.x for elf in elves]
    ys = [elf.y for elf in elves]
    w = max(xs) - min(xs) + 1
    h = max(ys) - min(ys) + 1
    return w * h - len(elves)
