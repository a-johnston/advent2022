from itertools import cycle


empty_row = 0b0
left_wall = 0b1000000
right_wall = 0b0000001

rocks = [
    # Horizontal bar shape
    [0b0011110],
    # Plus shape
    [0b0001000,
     0b0011100,
     0b0001000],
    # Corner shape
    [0b0011100,
     0b0000100,
     0b0000100],
    # Vertical bar shape
     [0b0010000] * 4,
    # Box shape
    [0b0011000,
     0b0011000],
]


class counting_cycle:
    def __init__(self, l):
        self.i = cycle(l)
        self.m = len(l)
        self.c = 0

    def __next__(self):
        self.c = (self.c + 1) % self.m
        return next(self.i)


def print_grid(grid, limit=None):
    limit = limit or len(grid)
    for idx in reversed(range(limit)):
        print(f'{grid[idx]:0>7b}'.replace('0', '.').replace('1', '#'))


def max_height(grid):
    for idx in reversed(range(len(grid))):
        if grid[idx] > 0:
            return idx + 1
    return 0


def resize_and_get_coord(grid, rock):
    y = max_height(grid) + 3 + len(rock)
    if len(grid) < y:
        for _ in range(y - len(grid)):
            grid.append(empty_row)
    return y - len(rock)


def collides(grid, rock, y):
    for yoff, row in enumerate(rock):
        if grid[y + yoff] & rock[yoff]:
            return True
    return False


def place(grid, rock, y):
    for yoff, row in enumerate(rock):
        grid[y + yoff] |= rock[yoff]


def sim(grid, wind_iter, rock_iter):
    rock = list(next(rock_iter))
    y = resize_and_get_coord(grid, rock)
    while True:
        wind = next(wind_iter)
        if wind == '<':
            if not any(r & left_wall for r in rock):
                shifted = [r << 1 for r in rock]
                if not collides(grid, shifted, y):
                    rock = shifted
        elif not any(r & right_wall for r in rock):
            shifted = [r >> 1 for r in rock]
            if not collides(grid, shifted, y):
                rock = shifted
        if collides(grid, rock, y - 1) or y == 0:
            place(grid, rock, y)
            break
        y -= 1


def solve(lines, arg=2022):
    grid = []
    wind_iter = counting_cycle(next(lines))
    rock_iter = counting_cycle(rocks)

    rounds = int(arg)
    deltas = {}
    height = 0
    match_run = []
    run_delta = -1
    run_start = -1

    for idx in range(rounds):
        key = (rock_iter.c, wind_iter.c)
        sim(grid, wind_iter, rock_iter)
        delta = max_height(grid) - height
        height += delta
        old_delta, old_idx = deltas.get(key, (-1, -1))
        deltas[key] = (delta, idx)
        if match_run:
            if old_delta == delta:
                if (idx - run_start) == run_delta:
                    break
                match_run.append(delta)
            else:
                match_run.clear()
                run_start = -1
                run_delta = -1
        if not match_run:
            if old_delta == delta:
                match_run.append(delta)
                run_delta = (idx - old_idx) * 2
                run_start = idx
    if idx != rounds - 1:
        full_loops = int((rounds - idx) / len(match_run))
        height += sum(match_run) * full_loops
        leftover = rounds - len(match_run) * full_loops - idx
        # Because of how the height is tracked and the loop is broken out of, we've
        # effectively already counted match_run[0] an extra time
        if leftover > 0:
            height += sum(match_run[1:leftover])
        else:
            height -= match_run[0]
    return height
