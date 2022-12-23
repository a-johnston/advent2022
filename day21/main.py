from operator import add, sub as lsub, mul, floordiv as ldiv


rdiv = lambda a, b: ldiv(b, a)
rsub = lambda a, b: lsub(b, a)


# 3-tuple representing ops such that (a = op(b, c), b = op(a, c), c = op(b, a))
ops = {
    '+': (add, lsub, rsub),
    '-': (lsub, add, lsub),
    '*': (mul, ldiv, rdiv),
    '/': (ldiv, mul, ldiv),
}


def maybe_solve(node):
    if node.left is None and node.right is None:
        return node.val is not None

    op = node.op
    a, b, c = node.val, node.left.val, node.right.val
    if op == '=':
        for v in (a, b, c):
            if v is not None:
                a, b, c = v, v, v
    else:
        if a is None:
            if b is not None and c is not None:
                a = ops[op][0](b, c)
        elif b is None:
            if c is not None:
                b = ops[op][1](a, c)
        elif c is None:
            c = ops[op][2](b, a)

    node.val, node.left.val, node.right.val = a, b, c
    return a is not None and b is not None and c is not None


class Node:
    def __init__(self, line):
        self.name, line = line.split(': ')
        self.env = None
        self.parent = None
        if line.isnumeric():
            self.val = int(line)
            self.left = None
            self.right = None
            self.op = None
        else:
            self.val = None
            self.left, self.op, self.right = line.split()

    def set_env(self, env):
        self.env = env
        if self.left:
            self.left = env[self.left]
            self.left.parent = self
        if self.right:
            self.right = env[self.right]
            self.right.parent = self


def load_env(lines):
    env = {}
    for line in lines:
        node = Node(line)
        env[node.name] = node
    for node in env.values():
        node.set_env(env)
    return env


def _maybe_visit_others(ignore, primary, secondary, node, use_secondary=False):
    for other in (node.left, node.right, node.parent):
        if other is not None and other not in ignore:
            if other in secondary:
                if use_secondary:
                    return
                secondary.remove(other)
            if other not in primary:
                primary.append(other)


def get_value_for(env, name):
    edge = [env[name]]
    revisit = []
    solved = {node for node in env.values() if node.val is not None}

    while edge:
        node = edge.pop()
        if node in revisit:
            revisit.remove(node)
        if not edge:
            edge, revisit = revisit, edge
        if node in solved:
            continue

        if maybe_solve(node):
            solved.add(node)
            _maybe_visit_others(solved, edge, revisit, node)
        else:
            revisit.append(node)
            _maybe_visit_others(solved, edge, revisit, node, use_secondary=True)
    return env[name].val


def solve_p1(lines):
    env = load_env(lines)
    return get_value_for(env, 'root')


def solve_p2(lines):
    env = load_env(lines)
    env['root'].op = '='
    env['humn'].val = None
    return get_value_for(env, 'humn')
