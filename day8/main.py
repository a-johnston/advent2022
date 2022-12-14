class Solver:
    def __init__(self):
        self.grid = None
        self.w = None
        self.h = None

    def parse(self, lines):
        self.grid = []
        for line in lines:
            if not line:
                continue
            self.grid.append([int(c) for c in line])
        self.w = len(self.grid[0])
        self.h = len(self.grid)

    def invalid(self, n):
        x, y = n
        return x < 0 or x >= self.w or y < 0 or y >= self.h

    def solve(self, lines):
        raise NotImplementedError

class PartOne(Solver):
    def __init__(self):
        super().__init__()
        self.visible = None

    def parse(self, lines):
        super().parse(lines)
        self.visible = [[0] * len(row) for row in self.grid]

    def cast(self, sx, sy, dx, dy):
        block = -1
        x, y = sx, sy
        while not self.invalid((x, y)):
            val = self.grid[y][x]
            if val > block:
                self.visible[y][x] = 1
                block = val
            x += dx
            y += dy

    def solve(self, lines):
        self.parse(lines)

        for x, dx in ((0, 1), (self.w - 1, -1)):
            for y in range(self.h):
                self.cast(x, y, dx, 0)

        for y, dy in ((0, 1), (self.h - 1, -1)):
            for x in range(self.w):
                self.cast(x, y, 0, dy)

        return sum(sum(row) for row in self.visible)

solve_p1 = PartOne().solve


class PartTwo(Solver):
    def cast(self, x, y, dx, dy):
        block = self.grid[y][x]
        x, y = x + dx, y + dy
        score = 0
        while not self.invalid((x, y)):
            val = self.grid[y][x]
            if val >= block:
                return score + 1
            x, y = x + dx, y + dy
            score += 1
        return score

    def gen_scores(self):
        for x in range(self.w):
            for y in range(self.h):
                x1 = self.cast(x, y, 1, 0)
                x2 = self.cast(x, y, -1, 0)
                y1 = self.cast(x, y, 0, 1)
                y2 = self.cast(x, y, 0, -1)
                yield x1 * x2 * y1 * y2

    def solve(self, lines):
        self.parse(lines)
        return max(self.gen_scores())


solve_p2 = PartTwo().solve
