import heapq
import re
from functools import lru_cache
from itertools import product


ntn = {}
flow = {}


def funny_name(name):
    v = 0
    for c in name:
        v *= 26
        v += ord(c) - ord('A')
    return v


def get_ntn_cost(graph):
    for n1, edges in graph.items():
        ntn[(n1, n1)] = 0
        check = {(1, edge) for edge in edges}
        while check:
            d, n2 = check.pop()
            key = (n1, n2)
            if key not in ntn or d < ntn[key]:
                ntn[key] = d
                for n3 in graph[n2]:
                    check.add((d + 1, n3))


def parse_graph(lines):
    graph = dict()
    for line in lines:
        parts = line.replace(',', '').split()
        name = funny_name(parts[1])
        val = int(parts[4][5:-1])
        if val > 0:
            flow[name] = val  # Only track nonzero flow
        idx = parts.index('valves') + 1 if 'valves' in parts else -1
        graph[name] = tuple(map(funny_name, parts[idx:]))
    get_ntn_cost(graph)


@lru_cache(None)
def intro_to_algorithms(time, places, valves=frozenset()):
    if time < 2:
        return 0
    all_options = []
    for place in places:
        if isinstance(place, tuple):
            if place[1] == 0:
                place = place[0]
            else:
                all_options.append([((place[0], place[1] - 1), 0)])
                continue
        options = []
        for other, subflow in flow.items():
            if other in valves:
                continue
            cost = ntn[(place, other)]
            benefit = subflow * (time - cost - 1)
            if cost + 2 > time:
                continue
            if cost == 0:
                options.append((other, benefit))
            else:
                options.append(((other, cost), benefit))
        all_options.append(options)

    best = 0
    for options in product(*all_options):
        min_wait = 100
        places = tuple()
        score = 0
        new_valves = valves
        for place, node_score in options:
            if isinstance(place, tuple):
                key = place[0]
                if place[1] < min_wait:
                    min_wait = place[1]
            else:
                key = place
                min_wait = 0
            if node_score > 0:
                if key in new_valves:
                    break
                new_valves |= {key}
                score += node_score
            places += (place,)
        if len(places) != len(options):
            continue  # Multiple actors open the same valve with this option
        if min_wait < time and min_wait > 0:
            places = tuple((a, b - min_wait) for a, b in places)
        score += intro_to_algorithms(time - 1 - min_wait, places, new_valves)
        if score > best:
            best = score
    return best


def setup(lines):
    intro_to_algorithms.cache_clear()
    flow.clear()
    ntn.clear()
    parse_graph(lines)


def solve_p1(lines):
    setup(lines)
    return intro_to_algorithms(30, (0,))


def solve_p2(lines):
    setup(lines)
    return intro_to_algorithms(26, (0, 0))
