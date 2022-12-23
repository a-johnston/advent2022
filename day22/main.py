dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))


def wrap(grid, x, y):
    return x % len(grid[0]), y % len(grid)


def move_p1(grid, x, y, d):
    nx, ny = wrap(grid, x + dirs[d][0], y + dirs[d][1])
    while grid[ny][nx] == ' ':
        nx, ny = wrap(grid, nx + dirs[d][0], ny + dirs[d][1])
    if grid[ny][nx] == '#':
        return x, y, d, True
    return nx, ny, d, False


def move_p2(grid, x, y, d):
    return x, y, d, True


def _count(grid, x, y):
    adjacent = (wrap(grid, (x + dx, y + dy)) for dx, dy in dirs)
    return sum(int(grid[y][x] != ' ') for x, y in adjacent)

def grid_post_p2(grid):
    pass


def _solve(lines, move, grid_post=None):
    grid = []
    moves = None
    maxw = 0
    for line in lines:
        if not line:
            moves = next(lines)
        else:
            grid.append(list(line))
            maxw = max(maxw, len(line))

    for idx, val in enumerate(grid):
        if len(val) < maxw:
            grid[idx] += ' ' * (maxw - len(val))

    if grid_post:
        grid_post(grid)

    y = 0
    for i, v in enumerate(grid[0]):
        if v == '.':
            x = i
            break

    d = 0
    v = 0
    for m in moves:
        if m.isnumeric():
            v *= 10
            v += int(m)
        else:
            for _ in range(v):
                x, y, d, hit = move(grid, x, y, d)
                if hit:
                    break
            v = 0
            if m == 'R':
                d = (d + 1) % len(dirs)
            elif m == 'L':
                d = (d - 1) % len(dirs)
            else:
                raise ValueError(m)
    for _ in range(v):
        x, y, d, hit = move(grid, x, y, d)
        if hit:
            break
    return 1000 * (y + 1) + 4 * (x + 1) + d


def solve_p1(lines):
    return _solve(lines, move_p1)


def solve_p2(lines):
    return _solve(lines, move_p2, grid_post_p2)
