from collections import defaultdict
from itertools import product


def parse(lines):
    cubes = []
    grid = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for line in lines:
        x, y, z = map(int, line.split(','))
        cubes.append((x, y, z))
        grid[x][y][z] += 1
    return cubes, grid


options = (-1, 0, 1)
def adjacent(x, y, z):
    for xx, yy, zz in product(options, options, options):
        if abs(xx) + abs(yy) + abs(zz) == 1:
            yield x + xx, y + yy, z + zz


def solve_p1(lines):
    cubes, grid = parse(lines)
    faces = 0
    options = (-1, 0, 1)
    for x, y, z in cubes:
        for xx, yy, zz in adjacent(x, y, z):
            if grid[xx][yy][zz] == 0:
                faces += 1
    return faces


def solve_p2(lines):
    cubes, grid = parse(lines)
    faces = 0
    space_min = (
        min(c[0] for c in cubes) - 1,
        min(c[1] for c in cubes) - 1,
        min(c[2] for c in cubes) - 1,
    )
    space_max = (
        max(c[0] for c in cubes) + 1,
        max(c[1] for c in cubes) + 1,
        max(c[2] for c in cubes) + 1,
    )
    edge = {space_min}
    seen = set()
    while edge:
        xyz = edge.pop()
        if xyz in seen:
            continue
        seen.add(xyz)
        for x, y, z in adjacent(*xyz):
            if x < space_min[0] or y < space_min[1] or z < space_min[2]:
                continue
            if x > space_max[0] or y > space_max[1] or z > space_max[2]:
                continue
            if grid[x][y][z] == 0:
                edge.add((x, y, z))
            else:
                faces += 1
    return faces
