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
    """
    Return the URL of the **cachai** datasets repository.

    Returns
        :class:`str`
            GitHub URL of the dataset repository.

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.data as chd

        print(chd.get_dataset_repo())

    .. code-block:: text
        :class: out-block

        https://github.com/DD-Beltran-F/cachai-datasets
    """
    return 'https://github.com/DD-Beltran-F/cachai-datasets'

def get_dataset_names():
    """
    Retrieve the list of available dataset names.

    Returns
        :class:`list` of :class:`str`
            Names of the datasets available in the catalog.

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.data as chd

        print(chd.get_dataset_names())

    .. code-block:: text
        :class: out-block

        ["lithium", "correlations", "correlations_big"]
    """
    catalog = _get_datasets_catalog(True)
    return list(catalog.keys())

def get_dataset_metadata(name):
    """
    Print the metadata of a specific dataset.

    Parameters
        name : :class:`str`
            Name of the dataset.

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.data as chd

        chd.get_dataset_metadata('lithium')

    .. code-block:: text
        :class: out-block

        ══════════════════════════════════════════════════════════════════════════════════════════
        METADATA OF DATASET: LITHIUM
        ──────────────────────────────────────────────────────────────────────────────────────────
        Alias       : lithium
        Filename    : lithium.csv
        Description : Data of lithium abundances and stellar parameters from  M. L. L. Dantas et
                      al. (2025) doi: 10.1051/0004-6361/202453034
        Columns     : CNAME, [Fe/H], A(Li), \\overline{t}_{\\star}, M, T_{eff}, e, Z_{max}, L_z
        ══════════════════════════════════════════════════════════════════════════════════════════
    """
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

def load_dataset(name="",redownload=False):
    """
    Load a dataset from GitHub with a persistent cache system.

    Parameters
        name : :class:`str`
            Name of the dataset to load.
        redownload : :class:`bool`, optional
            Whether to force re-downloading the dataset, ignoring the cache
            (default: ``False``).

    Returns
        :class:`pandas.DataFrame`
            DataFrame containing the dataset.

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.data as chd

        df = chd.load_dataset('lithium')
        print(df.head())

    .. code-block:: text
        :class: out-block

                      CNAME  [Fe/H]  A(Li)  ...         e  Z$_{max}$        $L_z$
        0  00000302-6002570   -0.31   2.01  ...  0.119362   1.003228  2028.535804
        1  00001749-5449565   -0.17   1.98  ...  0.110635   0.670432  1907.144965
        2  00012216-5458205   -0.07   1.51  ...  0.276396   0.996552  1836.529851
        3  00040666-3709129    0.28   0.62  ...  0.112774   0.501939  1676.768299
        4  00042981-4701022   -0.34   1.71  ...  0.257109   1.327526  2239.902280

        [5 rows x 9 columns]
        ...
    """
    catalog = _get_datasets_catalog(redownload)
    
    if name not in catalog:
        raise ValueError(f"Dataset '{name}' does not exist. "
                         f"The current valid datasets are: {', '.join(get_dataset_names())}.")
    
    url = DATASETS_REPO + catalog[name]['filename']
    cached_file = _download_with_cache(url, redownload)
    
    return pd.read_csv(cached_file)

def clear_cache(max_age_days=0):
    """
    Delete old cached files from **cachai**'s cache directory.

    Parameters
        max_age_days : :class:`int`, optional
            Maximum file age in days. Files older than this will be deleted.
            If set to ``0`` (default), all files are removed.

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.data as chd

        # Delete all cached files
        chd.clear_cache()

    .. code-block:: text
        :class: out-block

        3 file(s) deleted by 2025-09-29 (14:43:47) from cachai's cache folder.
        Space freed: 153.1 KB (100.0%).
    
    You can also choose the maximum file age in days, files older than ``max_age_days`` will be
    deleted:

    .. code-block:: python
        :class: mock-block

        import cachai.data as chd

        # Delete files older than 30 days
        clear_cache(max_age_days=30)
    """
    now         = time.time()
    counts      = 0
    total       = 0
    freed_space = 0
    
    total_space = sum(
        os.path.getsize(os.path.join(CACHE_DIR, f)) 
        for f in os.listdir(CACHE_DIR) 
        if os.path.isfile(os.path.join(CACHE_DIR, f)))

    if total_space == 0:
        print("cachai's cache folder is already empty.")
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
    print(f"{counts} file(s) deleted by {now_str} from cachai's cache folder.\n"
          f'Space freed: {sizeof_fmt(freed_space)} ({freed_space/total_space*100:.1f}%).')