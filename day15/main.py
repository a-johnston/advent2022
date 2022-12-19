import math
import re


pattern = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
matcher = re.compile(pattern)


def _parse(line):
    return map(int, matcher.match(line).groups())


def _parse_lines_to_header_and_sensors(lines, m = 1):
    header = int(next(lines)) * m
    sensors = []
    for line in lines:
        if not line:
            continue
        sx, sy, bx, by = _parse(line)
        db = _dist(sx, sy, bx, by)
        sensors.append((sx, sy, db))
    return header, sensors


def _dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def _merge(intervals):
    intervals = sorted(intervals)
    prev = intervals.pop(0)
    while intervals:
        node = intervals.pop(0)
        if node[0] <= prev[1]:
            prev = (prev[0], max(node[1], prev[1]))
        else:
            yield prev
            prev = node
    yield prev


def solve_p1(lines):
    y = int(next(lines))
    intervals = []
    for line in lines:
        if not line:
            continue
        sx, sy, bx, by = _parse(line)
        db = _dist(sx, sy, bx, by)
        dt = _dist(sx, sy, sx, y)
        if dt < db:
            n = db - dt
            if by == y:
                intervals.append((sx - n, bx))
                intervals.append((bx + 1, sx + n + 1))
            else:
                intervals.append((sx - n, sx + n + 1))
    return sum(b - a for a, b in _merge(intervals))


def _out_of_bounds(x, y, w):
    return x < 0 or y < 0 or x > w or y > w


def _move(x, y, m, w):
    if x < 0:
        return 0, y - x * m
    if y < 0:
        return x - y * m, 0
    if x > w:
        return w, y - (x - w) * m
    if y > w:
        return x - (y - w) * m, w
    return x, y


def _trim(x1, y1, x2, y2, m, w):
    x1, y1 = _move(x1, y1, m, w)
    x2, y2 = _move(x2, y2, m, w)
    if _out_of_bounds(x1, y1, w) or _out_of_bounds(x2, y2, w):
        return None
    return x1, y1, x2, y2, m


def _len(segment):
    return abs(segment[0] - segment[2]) + 1


def _get_intervals(x, y, r, w):
    # Generates non-overlapping line segments (x1, y1, x2, y2, m) where x1 < x2
    # and m is the slope; either -1 or 1. Each segment is 1 block outside of the
    # given sensor's radius.
    return tuple(filter(None, (
        _trim(x - r, y, x - 1, y - r + 1, -1, w),
        _trim(x, y - r, x + r - 1, y - 1, 1, w),
        _trim(x + 1, y + r - 1, x + r, y, -1, w),
        _trim(x - r + 1, y + 1, x, y + r, 1, w),
    )))


def _intersect(l, s):
    da = s[2] - _dist(l[0], l[1], s[0], s[1])
    db = s[2] - _dist(l[2], l[3], s[0], s[1])
    # fully contained
    if da >= 0 and db >= 0:
        return []
    # clips head
    if da >= 0:
        d = int((-db - 1) / 2)
        return [(l[2] - d, l[3] - d * l[4], l[2], l[3], l[4])]
    # clips tail
    if db >= 0:
        d = int((-da - 1) / 2)
        return [(l[0], l[1], l[0] + d, l[1] + d * l[4], l[4])]
    if l[0] < s[0] and s[0] < l[2] and min(l[1], l[3]) < s[1] and s[1] < max(l[1], l[3]):
        """ x1 = s[0]
            y1 = l[1] + (s[0] - l[0]) * l[4]

            x2 = l[0] + (s[1] - l[1]) * l[4]
            y2 = s[1]
        """
        # project sensor onto line to determine distance
        px = (s[0] + l[0] + (s[1] - l[1]) * l[4]) / 2
        py = (s[1] + l[1] + (s[0] - l[0]) * l[4]) / 2

        px1 = math.floor(px)
        py1 = math.floor(py)
        px2 = math.ceil(px)
        py2 = math.ceil(py)
        if l[4] == -1:
            py1, py2 = py2, py1
        d = s[2] - _dist(px1, py1, s[0], s[1])
        if d > 0:
            return [
                (l[0], l[1], px1 - d, py1 - d * l[4], l[4]),
                (px2 + d, py2 + d * l[4], l[2], l[3], l[4]),
            ]
    return [l]


def solve_p2(lines):
    w, sensors = _parse_lines_to_header_and_sensors(lines, 2)
    all_intervals = []
    for i, (x, y, r) in enumerate(sensors):
        all_intervals.append((i, _get_intervals(x, y, r + 1, w)))
    for i, intervals in all_intervals:
        for interval in intervals:
            subintervals = [interval]
            for j, sensor in enumerate(sensors):
                if i == j:
                    continue
                new = []
                for subinterval in subintervals:
                    new.extend(_intersect(subinterval, sensor))
                subintervals = new
            for interval in subintervals:
                if _len(interval) > 0:
                    return interval[0] * 4000000 + interval[1]


def test_add_interval(grid, interval, c):
    x, y = interval[0], interval[1]
    while x <= interval[2]:
        test_mark_grid(grid, x, y, c)
        x += 1
        y += interval[4]


def test_mark_grid(grid, x, y, c):
    try:
        grid[y][x] = c
    except:
        print(x, y, c)


def test_print_grid(grid):
    print('   ' + ''.join(str(x % 10) if x % 5 == 0 else ' ' for x in range(len(grid[0]))))
    for y in range(len(grid)):
        print(f'{y:<3}' + ''.join(grid[y]))
