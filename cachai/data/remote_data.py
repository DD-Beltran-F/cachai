import os
import time
import pandas as pd
import hashlib
import warnings
import json
from   urllib.request import urlopen, Request
from   urllib.error import URLError
from  ._utils import sizeof_fmt, CACHE_DIR, DATASETS_REPO, DATASETS_CATALOG

def _get_cache_path(url):
    """Generate cache path using URL hash"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, url_hash)

def _download_with_cache(url, force=False):
    """Download file with persistent cache system"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = _get_cache_path(url)
    
    if not force and os.path.exists(cache_path):
        return cache_path

    try:
        req = Request(url, headers={'User-Agent': 'CACHAI'})
        with urlopen(req) as response:
            data = response.read()
            with open(cache_path, 'wb') as f:
                f.write(data)
        return cache_path
    except URLError as e:
        # Fallback to existing cache
        if os.path.exists(cache_path):
            warnings.warn(f"Using cached version due to an error. Details: {str(e)}")
            return cache_path
        raise ConnectionError(f"Error downloading {url}. Details: {str(e)}")

def _get_datasets_catalog(force=False):
    """Obtain the dataset catalog from GitHub"""
    url = DATASETS_REPO + DATASETS_CATALOG
    cached_file = _download_with_cache(url, force)
    
    with open(cached_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_dataset_repo():
    """Return the dataset repository url"""
    return 'https://github.com/DD-Beltran-F/cachai-datasets'

def get_dataset_names():
    """Return a list with the available datasets names"""
    catalog = _get_datasets_catalog(True)
    return list(catalog.keys())

def get_dataset_metadata(name):
    """Print the metadata of a specific dataset"""
    catalog = _get_datasets_catalog(True)

    if name not in catalog:
        raise ValueError(f"Dataset '{name}' does not exist. "
                         f"The current valid datasets are: {', '.join(get_dataset_names())}.")

    dataset_meta = catalog[name]

    print('═'*50)
    print(f'METADATA OF DATASET: {name.upper()}')
    print('─'*50)
    print(f'Alias       : {name}')
    print(f"Filename    : {dataset_meta.get('filename', 'Not specified')}")
    print(f"Description : {dataset_meta.get('description', 'Not available')}")
    columns = dataset_meta.get('columns', 'Not specified')
    if isinstance(columns,list): columns = ', '.join(columns).replace('$','')
    print(f"Columns     : {columns}")
    print("═"*50 + "\n")

def load_dataset(name='', redownload=False):
    """
    Load datasets from GitHub with a persistent cache system
    
    Parameters:
    -----------
    name : str
        Name of the dataset
    redownload : bool
        Whether to force the re-download of the dataset, ignoring cache

    Returns:
    --------
    pandas.DataFrame
    """
    catalog = _get_datasets_catalog(redownload)
    
    if name not in catalog:
        raise ValueError(f"Dataset '{name}' does not exist. "
                         f"The current valid datasets are: {', '.join(get_dataset_names())}.")
    
    url = DATASETS_REPO + catalog[name]['filename']
    cached_file = _download_with_cache(url, redownload)
    
    return pd.read_csv(cached_file)

def clear_cache(max_age_days=0):
    """Delete old cached files"""
    now         = time.time()
    counts      = 0
    total       = 0
    freed_space = 0
    
    total_space = sum(
        os.path.getsize(os.path.join(CACHE_DIR, f)) 
        for f in os.listdir(CACHE_DIR) 
        if os.path.isfile(os.path.join(CACHE_DIR, f)))

    if total_space == 0:
        print("CACHAI's cache folder is already empty.")
        return

    if os.path.exists(CACHE_DIR):
        total = len(os.listdir(CACHE_DIR))
        for filename in os.listdir(CACHE_DIR):
            filepath = os.path.join(CACHE_DIR, filename)
            if os.stat(filepath).st_mtime < now - max_age_days * 86400:
                file_size = os.path.getsize(filepath)
                try:
                    os.remove(filepath)
                    counts += 1
                    freed_space += file_size
                except Exception as e:
                    warnings.warn(f'Could not delete {filepath}. Details: {str(e)}')
    
    now_str = time.strftime("%Y-%m-%d (%H:%M:%S)", time.localtime(now))
    print(f"{counts} file(s) deleted by {now_str} from CACHAI's cache folder.\n"
          f'Space freed: {sizeof_fmt(freed_space)} ({freed_space/total_space*100:.1f}%).')