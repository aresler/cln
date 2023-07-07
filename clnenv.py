#!/usr/local/bin/python3

import argparse
import configparser
import json
from pathlib import Path
from shutil import rmtree
from subprocess import Popen, PIPE, STDOUT

small_sep = '-----'


def clean_dir(target_dir, name):
    t = Path(target_dir)
    print(f'{name}\n{small_sep}\n')
    if any(t.iterdir()):
        print(f'{target_dir}:\n')
        for i in t.iterdir():
            print(i.name)

        inpt = input('\nDo you want to clean this folder? Y/N: ')

        if inpt in ['y', 'Y']:
            for i in t.iterdir():
                print(f'Removing {i}')
                if i.is_dir():
                    rmtree(i)
                else:
                    i.unlink()
            print('')
        else:
            print(f'Skipping...\n')
            return 0
    else:
        print(f'{target_dir} is empty...\n')


def clean_conda(conda_bin):
    sub = Popen([conda_bin, 'env', 'list', '--json'], stdout=PIPE)
    envs = json.loads(sub.stdout.read())['envs']

    print(f'conda\n{small_sep}\n')
    if len(envs) > 1:  # Supposedly first element is always a base env
        print(f'Found conda envs: \n')
        for env in envs[1:]:
            print(env)

        inpt = input('\nRemove all? Y/N: ')
        if inpt in ['y', 'Y']:
            for env in envs[1:]:
                s = Popen([conda_bin, 'env', 'remove', '-p', env], stdout=PIPE, stderr=STDOUT)
                print(s.stdout.read())
            print('')
        else:
            print('Skipping...\n')
            return 0
    else:
        print(f'No conda envs found...\n')


def main():
    f = Path(__file__)

    if f.is_symlink():
        project_root = f.readlink().parent
    else:
        project_root = f.parent

    config = configparser.ConfigParser()
    config.read(project_root / 'config.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, help='Cleaner target',
                        choices=['conda', 'poetry', 'pipenv', 'all'])
    args = parser.parse_args()

    match args.target:
        case 'conda':
            clean_conda(config['bin']['conda'])
        case 'poetry':
            clean_dir(config['env']['poetry'], 'poetry')
        case 'pipenv':
            clean_dir(config['env']['pipenv'], 'pipenv')
        case 'all':
            clean_conda(config['bin']['conda'])
            clean_dir(config['env']['poetry'], 'poetry')
            clean_dir(config['env']['pipenv'], 'pipenv')


if __name__ == '__main__':
    main()
