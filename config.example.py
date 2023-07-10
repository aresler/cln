from pathlib import Path

home = Path.home()

# bin
CONDA = Path('/Users/john/miniconda3/bin/conda')

# env
POETRY = Path('/Users/john/Library/Caches/pypoetry')
PIPENV = Path('/Users/john/.local/share/virtualenvs')

# A list of custom dirs to clear

DIRS = [
    ((home / 'dir'), None),
    ((home / 'dir2'), None),
    ((home / 'dir3'), ['.png', '.jpg', '.jpeg', '.mp4', '.mov']),
]
