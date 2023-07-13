from pathlib import Path

home = Path.home()

# Bin
CONDA = home / 'miniconda3/bin/conda'

# Env/Cache
POETRY = home / 'Library/Caches/pypoetry'
PIPENV = home / '.local/share/virtualenvs'

# Custom dirs
DIRS: list[(Path, list[str])] = [
    (home / 'dir', None),
    (home / 'dir2', None),
    (home / 'dir3', ['.png', '.jpg', '.jpeg', '.mp4', '.mov']),
]
