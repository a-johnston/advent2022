def solve(lines, knots = 2):
    knots = [[0, 0] for _ in range(int(knots))]
    seen = {(0, 0)}
    dirs = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
    }

    def move(d):
        knots[0][0] += d[0]
        knots[0][1] += d[1]
        for idx in range(1, len(knots)):
            prev = knots[idx - 1]
            knot = knots[idx]
            dx = prev[0] - knot[0]
            dy = prev[1] - knot[1]
            if abs(dx) > 1 or abs(dy) > 1:
                knot[0] += dx / (abs(dx) or 1)
                knot[1] += dy / (abs(dy) or 1)
        seen.add(tuple(knots[-1]))

    for line in lines:
        if not line:
            continue
        d, n = line.split()
        d = dirs[d]
        for _ in range(int(n)):
            move(d)

    return len(seen)
