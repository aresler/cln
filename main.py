#!/usr/local/bin/python3

import argparse
from config import *

from cleaner import DirCleaner, Filter, clean_conda


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hidden', action='store_true', help='Include hidden')

    sub = parser.add_subparsers(title='env')
    sub1 = sub.add_parser('env', help='Clear Python virtual environment')
    sub1.add_argument('-t', '--target', type=str, required=True, help='Cleaner target',
                      choices=['conda', 'poetry', 'pipenv', 'all'])

    args = parser.parse_args()

    if hasattr(args, 'target'):
        match args.target:
            case 'conda':
                clean_conda(CONDA)
            case 'poetry':
                c = DirCleaner(POETRY, Filter(), prompt=True)
                c.clean()
            case 'pipenv':
                c = DirCleaner(PIPENV, Filter())
                c.clean()
            case 'all':
                clean_conda(CONDA)
                c = DirCleaner(POETRY, Filter())
                c.clean()
                c1 = DirCleaner(PIPENV, Filter())
                c1.clean()
    else:
        for d in DIRS:
            p = d[0]
            filt = Filter(d[1], hidden=args.hidden)
            c = DirCleaner(p, filt)
            c.clean()
    print('Done!')


if __name__ == '__main__':
    main()
