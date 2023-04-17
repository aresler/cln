import argparse
import configparser
import os
import subprocess


def clean_dir(dir):
    # TODO: Parse dir content into a list and apply command to each item separately
    if dir:
        l = os.listdir(dir)
        print(l)
    else:
        print('No dir...')


def clean_conda():
    # TODO: Implement stdout parsing
    sub = subprocess.Popen(['conda', 'env', 'list'], stdout=subprocess.PIPE)
    print(sub.stdout.read())


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(project_dir + '/config.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, help='Clean target', choices=['conda', 'poetry'])
    args = parser.parse_args()

    match args.target:
        case 'conda':
            clean_conda()
        case 'poetry':
            clean_dir(config['envs']['poetry'])


if __name__ == '__main__':
    main()
