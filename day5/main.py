def solve(lines, flag=None):
    mode = 0
    stacks = []
    mapped = {}
    for line in lines:
        if not line:
            # Use empty line to escape setup mode
            mode = 1
            continue

        # Setup mode
        if mode == 0:
            # Pair each stack with its true number
            if line.startswith(' ') and not line.startswith('  '):
                vals = [int(c) for c in line if c != ' ']
                mapped = dict(zip(vals, stacks))
                continue

            # Init stacks
            if not stacks:
                stacks = [[] for _ in range(int((len(line) + 1) / 4))]

            # Build each stack bottom-up
            for idx, stack in enumerate(stacks):
                val = line[idx * 4 : idx * 4 + 4].strip('[] ')
                if val:
                    stack.insert(0, val)

        # Move mode
        if mode == 1:
            a, b = line.split(' from ')
            count = int(a.split(' ')[1])
            src, dst = map(int, b.strip().split(' to '))

            if flag:
                mapped[src], moved = mapped[src][:-count], mapped[src][-count:]
                mapped[dst] += moved
            else:
                for _ in range(count):
                    mapped[dst].append(mapped[src].pop())

    return ''.join(mapped[stack][-1] for stack in sorted(mapped))
