import math
from functools import lru_cache
from multiprocessing import Pool


resources = {'ore': 3, 'clay': 2, 'obsidian': 1, 'geode': 0}


def parse(lines, mode):
    blueprints = {}
    for line in lines:
        if mode and len(blueprints) == 3:
            break
        n, line = line.split(': ', 1)
        n = int(n[10:])
        blueprints[n] = {}
        for part in line.split('. '):
            costs = {}
            parts = part.strip('.').split()
            blueprints[n][resources[parts[1]]] = costs
            for i in range(4, len(parts)):
                if parts[i].isnumeric():
                    costs[resources[parts[i + 1]]] = int(parts[i])
    return blueprints


rules = {}
staff_maxes = {}


def set_rules(blueprint):
    rules.clear()
    rules.update(blueprint)
    intro_to_algorithms.cache_clear()
    staff_maxes.update({1: 0, 2: 0, 3: 0})

    for recipe in rules.values():
        for other, count in recipe.items():
            if count > staff_maxes[other]:
                staff_maxes[other] = count


def add_tuple(t, i, x):
    t = list(t)
    t[i] += x
    return tuple(t)


def mul_tuple(t, x):
    return tuple(x * y for y in t)

def add_tuples(*t):
    return tuple(sum(x) for x in zip(*t))


@lru_cache(None)
def intro_to_algorithms(time, staff, supply):
    if time < 1:
        return supply[0]

    # Figure out what we can buy
    states = []
    for kind, recipe in rules.items():
        if kind in staff_maxes and staff[kind] >= staff_maxes[kind]:
            continue
        new_supply = supply
        make_time = 0
        for resource, count in recipe.items():
            if staff[resource] == 0:
                break
            rounds = math.ceil((count - new_supply[resource]) / staff[resource])
            make_time = max(make_time, rounds)
            new_supply = add_tuple(new_supply, resource, -count)
        else:
            if make_time < time - 1:
                states.append((time - make_time - 1, add_tuple(staff, kind, 1), new_supply))
    if not states:
        return supply[0] + staff[0] * time

    # Add newly collected resources to possible states, adding the staff we start
    # with instead of the staff we potentially just built.
    for idx, (stime, sstaff, ssupply) in enumerate(states):
        ssupply = add_tuples(ssupply, mul_tuple(staff, time - stime))
        states[idx] = (stime, sstaff, ssupply)

    best = supply[0]
    for state in states:
        val = intro_to_algorithms(*state)
        if val > best:
            best = val
    return best


def _solve(time, idx, blueprint):
    set_rules(blueprint)
    val = intro_to_algorithms(time, (0, 0, 0, 1), (0, 0, 0, 0))
    print(idx, ':', val)
    if time > 30:
        return val
    return val * idx


def mul(vals):
    product = 1
    for val in vals:
        product *= val
    return product


def solve(lines, time=24, pool_size=None):
    time = int(time)
    total = 0
    mode = time > 30
    blueprints = parse(lines, mode)
    func = mul if mode else sum
    with Pool(int(pool_size) if pool_size else None) as pool:
        arglist = [(time, *item) for item in blueprints.items()]
        return func(pool.starmap(_solve, arglist))
