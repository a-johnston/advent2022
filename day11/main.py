from functools import reduce
from math import floor
from operator import add, mul


ops = {'+': add, '*': mul}


def _parse_op(op_str):
    l, op, r = op_str.split()
    def inner(x):
        return ops[op](
            x if l == 'old' else int(l),
            x if r == 'old' else int(r),
        )
    return inner


def _last_int(line):
    return int(line.rsplit(' ', 1)[1])


class Monkey:
    all_monkeys = {}

    @classmethod
    def get_monkey(cls, idx):
        if idx not in cls.all_monkeys:
            cls.all_monkeys[idx] = cls(idx)
        return cls.all_monkeys[idx]

    def __init__(self, idx):
        self.idx = idx
        self.items = []
        self.op = None
        self.div = None
        self.on_true = None
        self.on_false = None
        self.count = 0

    def parse(self, line):
        if line.startswith('  S'):
            self.items = list(map(int, line[18:].split(', ')))
        if line.startswith('  O'):
            self.op = _parse_op(line.split(' = ')[1])
        if line.startswith('  T'):
            self.div = _last_int(line)
        if 'true' in line:
            self.on_true = _last_int(line)
        if 'false' in line:
            self.on_false = _last_int(line)

    def take_turn(self, relief, global_mod):
        while self.items:
            self.count += 1
            item = self.op(self.items.pop(0)) % global_mod
            if relief != 1:
                item = floor(item / relief)
            target_id = self.on_true if item % self.div == 0 else self.on_false
            self.get_monkey(target_id).items.append(item)


def parse_lines(lines):
    Monkey.all_monkeys.clear()
    current_monkey = None

    for line in lines:
        if not line:
            continue
        if line.startswith('Monkey'):
            current_monkey = Monkey.get_monkey(int(line[7:-1]))
        else:
            current_monkey.parse(line)


def solve(lines, rounds=20, relief=3):
    parse_lines(lines)
    
    global_mod = reduce(mul, (m.div for m in Monkey.all_monkeys.values()))

    for idx in range(int(rounds)):
        for _, monkey in sorted(Monkey.all_monkeys.items()):
            monkey.take_turn(int(relief), global_mod)

    top = sorted(m.count for m in Monkey.all_monkeys.values())[-2:]
    return mul(*top)
