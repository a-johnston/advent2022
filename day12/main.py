def _solve_helper(lines, any_a):
    grid = []
    start = None
    end = None
    for idx, line in enumerate(lines):
        if not line:
            continue
        if 'S' in line:
            start = (line.find('S'), idx)
            line = line.replace('S', 'a')
        if 'E' in line:
            end = (line.find('E'), idx)
            line = line.replace('E', 'z')
        grid.append([ord(c) - ord('a') for c in line])

    w = len(grid[0])
    h = len(grid)

    def is_valid(x, y):
        return x >= 0 and x < w and y >= 0 and y < h

    nodes = [(*end, 0)]
    seen = set()
    while nodes:
        x, y, steps = nodes.pop(0)
        if (x, y) in seen:
            continue
        seen.add((x, y))

        if (grid[y][x] == 0) if any_a else ((x, y) == start):
            return steps

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and grid[y][x] - grid[ny][nx] < 2:
                nodes.append((nx, ny, steps + 1))


def solve_p1(lines):
    return _solve_helper(lines, False)


def solve_p2(lines):
    return _solve_helper(lines, True)
