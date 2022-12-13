_scores = {
    'A': 1,  # rock
    'X': 1,
    'B': 2,  # paper
    'Y': 2,
    'C': 3,  # scissors
    'Z': 3,
}


def solve_p1(lines):
    score = 0
    for line in lines:
        if not line:
            continue
        a, b = line.split()
        delta = _scores[b] - _scores[a]
        if delta == 0:
            bonus = 3
        elif delta == 1 or delta == -2:
            bonus = 6
        else:
            bonus = 0
        score += _scores[b] + bonus
    return score


def solve_p2(lines):
    score = 0
    for line in lines:
        if not line:
            continue
        a, b = line.split()
        if b == 'X':  # lose
            score += (_scores[a] - 1) or 3
        if b == 'Y':  # draw
            score += 3 + _scores[a]
        if b == 'Z':  # win
            score += 6 + (_scores[a] % 3) + 1
    return score
