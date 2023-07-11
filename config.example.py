from pathlib import Path

home = Path.home()

# bin
CONDA = home / 'miniconda3/bin/conda'

# env
POETRY = home / 'Library/Caches/pypoetry'
PIPENV = home / '.local/share/virtualenvs'

# A list of custom dirs to clear

DIRS = [
    ((home / 'dir'), None),
    ((home / 'dir2'), None),
    ((home / 'dir3'), ['.png', '.jpg', '.jpeg', '.mp4', '.mov']),
]
