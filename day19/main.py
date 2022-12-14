import math
from multiprocessing import Pool


resources = {'ore': 3, 'clay': 2, 'obsidian': 1, 'geode': 0}


class hashlist(list):
    def __hash__(self):
        h = 0
        for v in self:
            h *= 1000
            h += v
        return h


def parse(lines, limit=None):
    blueprints = {}
    for line in lines:
        if limit is not None and len(blueprints) == limit:
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
    record_result(0, True)

    staff_maxes.update({1: 0, 2: 0, 3: 0})
    for recipe in rules.values():
        for other, count in recipe.items():
            if count > staff_maxes[other]:
                staff_maxes[other] = count


blueprint_best = 0
def record_result(val, force=False):
    global blueprint_best
    if val > blueprint_best or force:
        blueprint_best = val
    return val


def should_discard(time, current):
    if time < 1:
        return True
    possible = current + math.floor((time - 1) * time / 2)
    return possible <= blueprint_best


def intro_to_algorithms(time, staff, supply):
    current_result = supply[0] + staff[0] * max(0, time)
    if should_discard(time, current_result):
        return record_result(current_result)

    # Figure out what we can buy
    states = []
    for kind, recipe in rules.items():
        if kind in staff_maxes and staff[kind] >= staff_maxes[kind]:
            continue
        new_supply = hashlist(supply)
        make_time = 0
        for resource, count in recipe.items():
            if staff[resource] == 0:
                break
            rounds = math.ceil((count - new_supply[resource]) / staff[resource])
            make_time = max(make_time, rounds)
            new_supply[resource] -= count
        else:
            if make_time < time - 1:
                new_staff = hashlist(staff)
                new_staff[kind] += 1
                states.append(hashlist([time - make_time - 1, new_staff, new_supply]))
    if not states:
        return record_result(current_result)

    # Add newly collected resources to possible states, adding the staff we start
    # with instead of the staff we potentially just built.
    for idx, state in enumerate(states):
        d = time - state[0]
        for i, x in enumerate(staff):
            state[2][i] += x * d

    best = current_result
    for state in states:
        val = intro_to_algorithms(*state)
        if val > best:
            best = val
    return record_result(best)


def _solve(time, idx, blueprint):
    set_rules(blueprint)
    val = intro_to_algorithms(time, (0, 0, 0, 1), (0, 0, 0, 0))
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
    if time > 30:
        blueprints = parse(lines, limit=3)
        func = mul
    else:
        blueprints = parse(lines)
        func = sum
    with Pool(int(pool_size) if pool_size else None) as pool:
        arglist = [(time, *item) for item in blueprints.items()]
        return func(pool.starmap(_solve, arglist))
