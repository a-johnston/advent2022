import os


class Node:
    all_nodes = {}

    @classmethod
    def make_node(cls, name, size=0):
        if name not in cls.all_nodes:
            cls.all_nodes[name] = cls(name=name, size=size)
        return cls.all_nodes[name]

    def __init__(self, name, size=0):
        self.name = name
        self._size=size
        self.children = []

    def is_dir(self):
        return self.name.endswith('/')

    def size(self):
        return self._size + sum(map(Node.size, self.children))

    def add_child(self, child):
        for other in self.children:
            if child.name == other.name:
                return
        self.children.append(child)


def parse_nodes(lines):
    Node.all_nodes.clear()
    pwd = '/'
    cnode = None
    for line in lines:
        if not line:
            continue
        if line.startswith('$ '):
            parts = line[2:].split(' ')
            if parts[0] == 'cd':
                if parts[1] == '..':
                    pwd = os.path.join(os.path.dirname(pwd.rstrip('/')), '')
                else:
                    pwd = os.path.join(pwd, parts[1], '')
                cnode = Node.make_node(pwd)
        else:
            a, b = line.split()
            name = os.path.join(pwd, b)
            if a == 'dir':
                cnode.add_child(Node.make_node(os.path.join(name, '')))
            else:
                cnode.add_child(Node.make_node(name, int(a)))

def solve_p1(lines):
    parse_nodes(lines)
    result = 0
    for node in Node.all_nodes.values():
        if node.is_dir() and (size := node.size()) <= 100000:
            result += size
    return result


def solve_p2(lines):
    total = 70000000
    needed = 30000000

    parse_nodes(lines)
    used = Node.make_node('/').size()
    target = needed - total + used
    best = total
    for node in Node.all_nodes.values():
        if node.is_dir() and (size := node.size()) >= target:
            if size < best:
                best = size
    return best
