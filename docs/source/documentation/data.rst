.. rst-class:: hide-me

Datasets (``cachai.data``)
====================================================================================================

.. raw:: html

   <div class="section-banner">
        <span class="section-banner-text">
            <i class="bi bi-book-half"></i> Documentation
        </span>
        <span class="section-banner-textadd">
            /Datasets
        </span>
   </div>

The ``cachai.data`` module allows you to access pre-created datasets hosted in the
`cachai-datasets GitHub <https://github.com/DD-Beltran-F/cachai-datasets>`_.
Downloading datasets requires an internet connection, if the files are already cached (i.e., you've
accessed them before), **cachai** will use the local copies, allowing offline work.

.. raw:: html

    <h2>Contents</h2>
    
.. currentmodule:: cachai.data

.. autosummary::
   :toctree: generated/
   :signatures: short
   
   load_dataset
   get_dataset_repo
   get_dataset_names
   get_dataset_metadata
   clear_cache