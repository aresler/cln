import argparse
import configparser
import subprocess
from pathlib import Path
from shutil import rmtree


def clean_dir(target_dir):
    path = Path(target_dir)
    for p in path.iterdir():
        print(f'Removing {p}')
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()


def clean_conda():
    # TODO: Implement stdout parsing
    sub = subprocess.Popen(['conda', 'env', 'list'], stdout=subprocess.PIPE)
    print(sub.stdout.read())


def main():
    project_dir = Path(__file__).parent
    config = configparser.ConfigParser()
    config.read(project_dir / 'config.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, help='Cleaner target', choices=['conda', 'poetry'])
    args = parser.parse_args()

    match args.target:
        case 'conda':
            clean_conda()
        case 'poetry':
            clean_dir(config['envs']['poetry'])


if __name__ == '__main__':
    main()
