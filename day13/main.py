from functools import cmp_to_key


def parse_list(s, c = 0):
    if s[c] != '[':
        raise ValueError(f'not a list {s} {c}')
    c += 1
    l = []
    n = 0
    while c < len(s):
        if s[c] == ']':
            return l, c + 1
        if s[c] == '[':
            sub, c = parse_list(s, c)
            l.append(sub)
        elif s[c] == ',':
            c += 1
        else:
            n = 0
            while s[c] not in ',]':
                n = n * 10 + int(s[c])
                c += 1
            l.append(n)
    raise ValueError(f'unclosed {s} {c}')


def cmp(a, b):  # -1 if a > b, 0 if a == b, 1 if a < b
    if isinstance(a, int) and isinstance(b, int):
        return int((b - a) / (abs(b - a) or 1))
    if isinstance(a, list) and isinstance(b, list):
        for ea, eb in zip(a, b):
            if (result := cmp(ea, eb)) != 0:
                return result
        return cmp(len(a), len(b))
    if isinstance(a, int):
        a = [a]
    else:
        b = [b]
    return cmp(a, b)


def solve_p1(lines):
    last = None
    idx = 1
    correct = []
    for line in lines:
        if not line:
            idx += 1
            last = None
        elif last is None:
            last = parse_list(line)[0]
        elif cmp(last, parse_list(line)[0]) > -1:
            correct.append(idx)
    return sum(correct)


def solve_p2(lines):
    packets = [[[2]], [[6]]]
    for line in lines:
        if line:
            packets.append(parse_list(line)[0])
    packets.sort(key=cmp_to_key(cmp), reverse=True)
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
