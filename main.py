#! /usr/bin/env python3
import importlib
import os
import sys


if __name__ == '__main__':
    day = sys.argv[1]
    mod = importlib.import_module(day + '.main')
    solvers = {}
    for name in dir(mod):
        if name.startswith('solve'):
            solver = getattr(mod, name)
            name = name[6:].replace('p', 'Part ')
            solvers[name] = solver
    if not solvers:
        print(f'bad module {mod.__name__}')
        sys.exit(1)

    print(' '.join(sys.argv[1:]))
    for name, solver in solvers.items():
        if name:
            print('\n' + name)
        for file in os.listdir(day):
            if not file.endswith('.txt'):
                continue
            with open(os.path.join(day, file)) as fp:
                solution = solver((l.rstrip('\n') for l in fp.readlines()), *sys.argv[2:])
                print(f'{file:<12}: {solution}')
