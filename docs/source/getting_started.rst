.. rst-class:: hide-me

|rocket-takeoff-fill| Getting Started
====================================================================================================

.. raw:: html

   <div class="section-banner">
        <span class="section-banner-text">
            <i class="bi bi-rocket-takeoff-fill"></i> Getting Started
        </span>
   </div>


You will typically use the following imports when working with **cachai**:

.. code-block:: python
    :class: mock-block

    import cachai as ch
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt


To quickly test **cachai**, you can load one of the included datasets. Currently, the available
datasets are tailored for **Chord Diagram** use cases. Here's a minimal example using the 
``correlations`` dataset to generate a Chord Diagram:

.. code-block:: python
    :class: mock-block

    import cachai.data as chd
    import cachai.chplot as chp

    data = chd.load_dataset('correlations')
    chp.chord(data)

.. note::
   
   Downloading datasets requires an internet connection. If the files are already cached (i.e.,
   you've accessed them before), **cachai** will use the local copies, allowing offline work.


.. hint::
   Want to learn how to use **cachai**? Check out the :doc:`examples section <../examples>`.