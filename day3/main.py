def char_score(c):
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27


def solve_p1(lines):
    score = 0
    for line in lines:
        if not line:
            continue
        half = int(len(line) / 2)
        score += sum(map(char_score, set(line[:half]) & set(line[half:])))
    return score


def solve_p2(lines):
    score = 0
    current = set()
    for idx, line in enumerate(lines):
        if current:
            current &= set(line)
        else:
            current = set(line)
        if (idx + 1) % 3 == 0:
            score += sum(map(char_score, current))
            current.clear()
    return score 
