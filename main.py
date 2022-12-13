#! /usr/bin/env python3
import importlib
import os
import sys


if __name__ == '__main__':
    day = sys.argv[1]
    mod = importlib.import_module(day + '.main')
    if hasattr(mod, 'solve'):
        solver = mod.solve
        args = sys.argv[2:]
    elif hasattr(mod, 'solve_p1') and hasattr(mod, 'solve_p2') and len(sys.argv) > 2:
        if '1' in str(sys.argv[-1]):
            solver = mod.solve_p1
        else:
            solver = mod.solve_p2
        args = sys.argv[2:-1]
    else:
        print(f'bad module {day}')
        sys.exit(1)

    print(' '.join(sys.argv[1:]))
    for file in os.listdir(day):
        if not file.endswith('.txt'):
            continue
        print(f'\n{file}:')
        with open(os.path.join(day, file)) as fp:
            print(' {}'.format(solver(map(str.strip, fp.readlines()), *args)))
