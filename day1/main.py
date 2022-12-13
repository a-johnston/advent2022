import sys


def solve(lines, topn):
    top_vals = []
    cval = 0
    for line in lines:
        if stripped := line.strip():
            cval += int(stripped)
        else:
            top_vals.append(cval)
            cval = 0
            if len(top_vals) > topn:
                top_vals.sort(reverse=True)
                top_vals = top_vals[:topn]
    return sum(top_vals)


if __name__ == '__main__':
    print(solve(sys.stdin, int(sys.argv[-1])))

