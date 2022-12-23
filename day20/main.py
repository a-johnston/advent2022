class Node:
    def __init__(self, val):
        self.val = val
        self.p = None
        self.n = None

    def get_node_at_offset(self, offset, m):
        offset %= m
        if offset > m / 2:
            offset -= m

        n = self
        while offset != 0:
            if offset > 0:
                n = n.n
                offset -= 1
            else:
                n = n.p
                offset += 1
        return n

    def move(self, m):
        self.p.n = self.n
        self.n.p = self.p
        # -1 reflects that we've "removed" this node from the lineup
        c = self.p.get_node_at_offset(self.val, m - 1)
        self.n = c.n
        self.p = c
        self.n.p = self
        self.p.n = self


def solve(lines, key=1, times=1):
    nodes = list(map(Node, (int(x) * int(key) for x in lines)))
    l = len(nodes)
    zero = None

    for i in range(l):
        if nodes[i].val == 0:
            zero = nodes[i]
        nodes[i].p = nodes[i - 1]
        nodes[i].n = nodes[(i + 1) % l]

    for _ in range(int(times)):
        for n in nodes:
            n.move(l)

    return sum((
        zero.get_node_at_offset(1000, l).val,
        zero.get_node_at_offset(2000, l).val,
        zero.get_node_at_offset(3000, l).val,
    ))
