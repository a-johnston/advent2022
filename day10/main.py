class Solver:
    default_result = 0

    def __init__(self):
        self.cycle = 0
        self.result = self.default_result
        self.x = 1

    def on_tick(self):
        pass

    def tick_clock(self):
        self.cycle += 1
        self.on_tick()

    def solve(self, lines):
        for line in lines:
            parts = line.strip().split()
            if not line:
                continue
            if parts[0] == 'noop':
                self.tick_clock()
            elif parts[0] == 'addx':
                self.tick_clock()
                self.tick_clock()
                self.x += int(parts[1])
        return self.result


class PartOne(Solver):
    check = {20, 60, 100, 140, 180, 220}

    def on_tick(self):
        if self.cycle in self.check:
            self.result += self.cycle * self.x


def solve_p1(lines):
    return PartOne().solve(lines)


class PartTwo(Solver):
    default_result = ''

    def on_tick(self):
        if abs(self.x - ((self.cycle - 1) % 40)) < 2:
            self.result += '█'
        else:
            self.result += ' '
        if self.cycle % 40 == 0:
            self.result += '\n'


def solve_p2(lines):
    return PartTwo().solve(lines)
