def solve(lines, l=4):
    l = int(l)
    solutions = []
    for line in lines:
        if not line:
            continue
        window = []
        for idx, c in enumerate(line):
            if len(window) < l:
                window.append(c)
            else:
                window[idx % l] = c
            if len(set(window)) == l:
                solutions.append(idx + 1)
                break
        else:
            print(f'No solution for {line}')
    return ', '.join(map(str, solutions))
