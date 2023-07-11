import json
from dataclasses import dataclass
from pathlib import Path
from shutil import rmtree
from subprocess import Popen, PIPE, STDOUT


@dataclass
class Filter:
    ext_list: list[str] | None = None
    hidden: bool = False


def remove_object(target: Path):
    print(f'Removing {target}...')
    if target.is_file():
        target.unlink()
    else:
        rmtree(target)


def clean_conda(conda_bin):
    sub = Popen([conda_bin, 'env', 'list', '--json'], stdout=PIPE)
    envs = json.loads(sub.stdout.read())['envs']

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


class DirCleaner:
    def __init__(self, target: Path, filt: Filter, prompt: bool = False):
        self.target = target
        self.filt = filt
        self.prompt = prompt

    def clean(self):
        print(f'{self.target}...')
        if not self.is_empty():
            go = self._ask() if self.prompt else True
            if go:
                for i in self.target.iterdir():
                    if (self.filt.ext_list and i.suffix in self.filt.ext_list) or (
                            not self.filt.ext_list and not (i.name.startswith('.') and not self.filt.hidden)):
                        remove_object(i)
                print()
            else:
                print('Skipping...')
        else:
            print('The directory is empty...\n')

    def is_empty(self):
        if any(self.target.iterdir()):
            return False
        else:
            return True

    def _ask(self):
        for i in self.target.iterdir():
            print(i.name)

        p = input('\nClear? Y/N: ')
        if p.lower() == 'y':
            return True
        else:
            return False
