.. rst-class:: hide-me

Testing
====================================================================================================

.. raw:: html

   <div class="section-banner">
        <span class="section-banner-text">
            <i class="bi bi-book-half"></i> Documentation
        </span>
        <span class="section-banner-textadd">
            /Testing
        </span>
   </div>

Tests can be run either in the terminal or in a Python/Jupyter file. It's recommended to use the
terminal with the ``cachai-test`` command. To see how to use the command and the available options,
simply run the command in your terminal with the option ``-h`` or ``--help`` as follows:

.. code-block:: console
    :class: in-block

    $ cachai-test -h
    
.. code-block:: console
    :class: out-block

    usage: cachai-test [OPTIONS] [TESTS...]

    Run the tests from CACHAI

    positional arguments:
    tests          Names of the tests to run (e.g. 'charts', 'utilities'). If
                    not specified, all tests are run.

    options:
    -h, --help     show this help message and exit
    -v, --verbose  Mostrar output detallado (equivalente a pytest -v)
    -l, --list     List all available tests without running them

.. raw:: html

    <h2>Contents</h2>

.. currentmodule:: cachai

.. autosummary::
    :toctree: generated/
    :signatures: short

    get_available_tests
    run_tests
