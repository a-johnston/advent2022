dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))


class Grid:
    def __init__(self, grid):
        self.grid = grid

    def get_start(self):
        y = 0
        for x, v in enumerate(self.grid[0]):
            if v == '.':
                return x, y, 1

    def move(self, x, y, d):
        raise NotImplementedError

    @classmethod
    def parse(cls, lines):
        grid = []
        moves_str = None
        maxw = 0
        for line in lines:
            if not line:
                moves_str = next(lines)
            else:
                grid.append(list(line))
                maxw = max(maxw, len(line))

        for idx, val in enumerate(grid):
            if len(val) < maxw:
                grid[idx] += ' ' * (maxw - len(val))

        moves = []
        v = 0
        for m in moves_str:
            if m.isnumeric():
                v *= 10
                v += int(m)
            else:
                moves.append(v)
                v = 0
                moves.append(m)
        if v > 0:
            moves.append(v)
        return cls(grid), moves


class GridP1(Grid):
    def wrap(self, x, y):
        return x % len(self.grid[0]), y % len(self.grid)


    def move(self, x, y, d):
        nx, ny = self.wrap(x + dirs[d][0], y + dirs[d][1])
        while self.grid[ny][nx] == ' ':
            nx, ny = self.wrap(nx + dirs[d][0], ny + dirs[d][1])
        if self.grid[ny][nx] == '#':
            return x, y, d, True
        return nx, ny, d, False


def _out_of_bounds(x, y, w, h):
    return x < 0 or y < 0 or x >= w or y >= h


# Describes faces with face 0 being "top", and the starting face, connected to
# 1-4 starting at the N edge and moving clockwise. Each of 1-4 has their "up"
# edge towards face 0. Face 6 is "bottom" and has its "up" edge aligned with
# face 1's "down" edge.
_face_edges = {
    0: (1, 2, 3, 4),
    1: (0, 4, 5, 2),
    2: (0, 1, 5, 3),
    3: (0, 2, 5, 4),
    4: (0, 3, 5, 1),
    5: (1, 4, 3, 2),
}


def _get_w(grid):
    for d in (3, 4):
        w = len(grid[0]) / d
        if int(w) == w:
            return int(w)


def _get_faces(grid):
    faces = {}
    w = _get_w(grid)
    print(len(grid[0]), w)
    y = 0
    for x in range(0, len(grid[0]), w):
        if grid[y][x] != ' ':
            faces[0] = (x, y, 0)

    edge = {0}
    seen = set()
    while edge:
        n = edge.pop()
        if n in seen:
            continue
        seen.add(n)
        x, y, d = faces[n]
        for nd, (dx, dy) in enumerate(dirs):
            nx = faces[n][0] + dx * w
            ny = faces[n][1] + dy * w
            if _out_of_bounds(nx, ny, len(grid[0]), len(grid)):
                continue
            if grid[ny][nx] == ' ':
                continue
            new_id = _face_edges[n][(d + nd) % len(dirs)]
            if new_id not in seen:
                new_d = (_face_edges[new_id].index(n) + nd + 2) % len(dirs)
                faces[new_id] = (nx, ny, new_d)
                edge.add(new_id)
    return faces


class GridP2(Grid):
    def __init__(self, grid):
        super().__init__(grid)
        self.faces = _get_faces(grid)
        print(self.faces)

    def move(self, x, y, d):
        return x, y, d, False


def _count(grid, x, y):
    adjacent = (wrap(grid, (x + dx, y + dy)) for dx, dy in dirs)
    return sum(int(grid[y][x] != ' ') for x, y in adjacent)


def sim_grid(grid, moves):
    x, y, d = grid.get_start()
    for m in moves:
        if m == 'R':
            d = (d + 1) % len(dirs)
        elif m == 'L':
            d = (d - 1) % len(dirs)
        else:
            for _ in range(m):
                x, y, d, hit = grid.move(x, y, d)
                if hit:
                    break
    print(x, y)
    return 1000 * (y + 1) + 4 * (x + 1) + (d - 1) % len(dirs)


def solve_p1(lines):
    grid, moves = GridP1.parse(lines)
    return sim_grid(grid, moves)


def solve_p2(lines):
    grid, moves = GridP2.parse(lines)
    return sim_grid(grid, moves)
