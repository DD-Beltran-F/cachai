.. rst-class:: hide-me

|gear-fill| Installation Guide
====================================================================================================

.. raw:: html

   <div class="section-banner">
        <span class="section-banner-text">
            <i class="bi bi-gear-fill"></i> Installation Guide
        </span>
   </div>


Installation
----------------------------------------------------------------------------------------------------

All official releases of **cachai** are published on `PyPI <https://pypi.org/project/cachai/>`_.
To install, simply run:

.. code-block:: console
    :class: mock-block

    $ pip install cachai

If you want to verify that **cachai** works correctly on your system, you can install it with
the optional testing dependencies:

.. code-block:: console
    :class: mock-block

    $ pip install cachai[testing]


Requirements
----------------------------------------------------------------------------------------------------

**cachai** has been tested on ``Python >= 3.10``.

**Core dependencies**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Python packages are mandatory:

    - `numpy <https://numpy.org>`_ ``>= 2.0.0``
    - `matplotlib <https://matplotlib.org>`_ ``>= 3.9.0``
    - `pandas <https://pandas.pydata.org>`_ ``>= 2.3.0``
    - `scipy <https://scipy.org>`_ ``>= 1.13.0``
    - `seaborn <https://seaborn.pydata.org/index.html>`_ ``>= 0.12.0``

**Optional dependencies**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Python packages are optional:

    - `pytest <https://docs.pytest.org/en/stable/>`_ ``>= 7.1.0`` *Only required for testing*

Verification
----------------------------------------------------------------------------------------------------

To verify that **cachai** installed correctly and is functioning properly on your system,
you can run:

.. code-block:: python
    :class: mock-block

    import cachai

    cachai.run_tests()

Alternatively, execute this in your terminal:

.. code-block:: console
    :class: mock-block

    $ cachai-test
