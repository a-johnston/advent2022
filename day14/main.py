AIR = 0
ROCK = 1
SAND = 2

def solve(lines, floor=False):
    rocks = []
    for line in lines:
        parts = line.split(' -> ')
        parts = [list(map(int, part.split(','))) for part in parts]
        rocks.append(parts)

    min_x = min(min(p[0] for p in r) for r in rocks)
    max_x = max(max(p[0] for p in r) for r in rocks)
    max_y = max(max(p[1] for p in r) for r in rocks)

    w = max_x - min_x + 1
    h = max_y + 1

    if floor:
        h += 2
        min_x -= h
        w += 2 * h

    grid = [[AIR] * w for _ in range(h)]

    if floor:
        for x in range(w):
            grid[-1][x] = ROCK

    def valid(x, y):
        return x >= 0 and x < w and y >= 0 and y < h

    # Offset all coordintes to fall within grid
    for rock in rocks:
        for part in rock:
            part[0] -= min_x

    # Fill grid with rock
    for rock in rocks:
        x, y = rock[0]
        for nx, ny in rock[1:]:
            dx = int((nx - x) / (abs(nx - x) or 1))
            dy = int((ny - y) / (abs(ny - y) or 1))
            grid[ny][nx] = ROCK

            while (x, y) != (nx, ny):
                grid[y][x] = ROCK
                x, y = x + dx, y + dy

    # Drop sand
    moves = ((0, 1), (-1, 1), (1, 1))
    def sim_sand():
        x, y = 500 - min_x, 0
        while valid(x, y) and grid[y][x] == AIR:
            for dx, dy in moves:
                if not valid(x + dx, y + dy):
                    return False
                if grid[y + dy][x + dx] == AIR:
                    x += dx
                    y += dy
                    break
            else:
                grid[y][x] = SAND
                return True
        return False

    count = 0
    while sim_sand():
        count += 1

    return count
