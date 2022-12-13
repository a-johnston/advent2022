def parse(line):
    a, b = line.split(',')
    return *map(int, a.split('-')), *map(int, b.split('-'))


def solve_p1(lines):
    count = 0
    for line in lines:
        if not line:
            continue
        a1, a2, b1, b2 = parse(line)
        # prevent interval A from being larger than interval B
        if a2 - a1 > b2 - b1:
            a1, a2, b1, b2 = b1, b2, a1, a2
        if a1 >= b1 and a2 <= b2:
            count += 1
    return count


def solve_p2(lines):
    count = 0
    for line in lines:
        if not line:
            continue
        a1, a2, b1, b2 = parse(line)
        # prevent interval A from starting after interval B
        if a1 > b1:
            a1, a2, b1, b2 = b1, b2, a1, a2
        if a2 >= b1:
            count += 1
    return count
