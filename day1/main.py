def solve(lines, topn=1):
    topn = int(topn)
    top_vals = []
    cval = 0
    for line in lines:
        if line:
            cval += int(line)
        else:
            top_vals.append(cval)
            cval = 0
            if len(top_vals) > topn:
                top_vals.sort(reverse=True)
                top_vals = top_vals[:topn]
    return sum(top_vals)
