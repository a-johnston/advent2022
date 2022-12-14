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
    elif all((
        len(sys.argv) > 2,
        sys.argv[-1].startswith('p'),
        hasattr(mod, f'solve_{sys.argv[-1]}'),
    )):
        solver = getattr(mod, f'solve_{sys.argv[-1]}')
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
            solution = solver((l.rstrip('\n') for l in fp.readlines()), *args)
            print(f' {solution}')
