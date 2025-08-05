import os
from   pathlib import Path

CACHE_DIR        = os.path.join(Path.home(), '.cachai_cache')
DATASETS_REPO    = 'https://raw.githubusercontent.com/DD-Beltran-F/cachai-datasets/main/'
DATASETS_CATALOG = 'datasets_catalog.json'

def sizeof_fmt(num,suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"