#!/usr/local/bin/python3

import argparse
import configparser
import json
from pathlib import Path
from shutil import rmtree
from subprocess import Popen, PIPE, STDOUT


def clean_dir(target_dir):
    path = Path(target_dir)
    for p in path.iterdir():
        print(f'Removing {p}')
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()


def clean_conda(conda_bin):
    sub = Popen([conda_bin, 'env', 'list', '--json'], stdout=PIPE)
    envs = json.loads(sub.stdout.read())

    for env in envs['envs'][1:]:
        s = Popen([conda_bin, 'env', 'remove', '-p', env], stdout=PIPE, stderr=STDOUT)
        print(s.stdout.read())


def main():
    # The script meant to run from a symlink, thus readlink() is used.
    project_dir = Path(__file__).readlink().parent
    config = configparser.ConfigParser()
    config.read(project_dir / 'config.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, help='Cleaner target',
                        choices=['conda', 'poetry', 'pipenv', 'all'])
    args = parser.parse_args()

    match args.target:
        case 'conda':
            clean_conda(config['bin']['conda'])
        case 'poetry':
            clean_dir(config['env']['poetry'])
        case 'pipenv':
            clean_dir(config['env']['pipenv'])
        case 'all':
            clean_conda(config['bin']['conda'])
            clean_dir(config['env']['poetry'])
            clean_dir(config['env']['pipenv'])


if __name__ == '__main__':
    main()
