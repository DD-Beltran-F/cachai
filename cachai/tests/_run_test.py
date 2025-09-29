import sys
import matplotlib.pyplot as plt
from   pathlib import Path
from   importlib.util import find_spec

def get_available_tests():
    """
    Retrieve the list of available test modules.

    Returns
        :class:`list` of :class:`str`
            Names of the available tests (retrieved from the test files without the
            ``test_`` prefix).

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    If you are running tests in the terminal, you can run ``cachai-test`` using the ``-l`` or
    ``--list`` option:
    
    .. code-block:: console
        :class: in-block

        $ cachai-test -l
    
    .. code-block:: console
        :class: out-block

        Available tests:
            utilities
            data
            dependencies
            gadgets
            charts
    
    If you are working in a Python/Jupyter file:

    .. code-block:: python
        :class: in-block

        import cachai as ch

        tests = ch.get_available_tests()
        print("Available tests:", tests)

    .. code-block:: text
        :class: out-block

        Available tests: ['utilities', 'data', 'dependencies', 'gadgets', 'charts']
    
    """
    test_dir = Path(__file__).parent
    return [f.stem[5:] for f in test_dir.glob('test_*.py')]

def run_tests(*test_args,show_details=False):
    """
    Run **cachai**'s test suite using pytest.

    Parameters
        test_args : :class:`str`
            Names of the tests to run (e.g., ``'charts'``, ``'utilities'``).
            If not provided, all available tests will be executed.
        show_details : :class:`bool`, optional
            Whether to include verbose output (``-v``) in pytest execution
            (default: ``True``).
    
    Returns
        :class:`int`
            Exit code returned by pytest.
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    There are two ways to run the cachai tests. It's recommended to do so from the terminal,
    as follows:

    .. code-block:: console
        :class: in-block

        $ cachai-test
    
    .. code-block:: console
        :class: out-block

        ================================ test session starts =================================
        platform linux -- Python 3.12.3, pytest-8.4.1, pluggy-1.6.0 -- /path_to_interpreter
        rootdir: /home/user
        plugins: anyio-4.10.0
        collected 57 items

        path_to_packages/cachai/tests/test_charts.py ...........................        [ 47%]
        path_to_packages/cachai/tests/test_data.py .......                              [ 59%]
        path_to_packages/cachai/tests/test_dependencies.py .....                        [ 68%]
        path_to_packages/cachai/tests/test_gadgets.py .....                             [ 77%]
        path_to_packages/cachai/tests/test_utilities.py .............                   [100%]

        ================================ 57 passed in 11.89s =================================
    
    You can also run a specific test from the list of available tests, and select the verbose
    option for more details.

    .. code-block:: console
        :class: in-block

        $ cachai-test utilities
    
    .. code-block:: console
        :class: out-block

        ================================= test session starts ==================================
        platform linux -- Python 3.12.3, pytest-8.4.1, pluggy-1.6.0 -- /path_to_interpreter
        cachedir: .pytest_cache
        rootdir: /home/user
        plugins: anyio-4.10.0
        collected 13 items                                                                                                                                                                   

        path_to_packages/cachai/tests/test_utilities.py::test_validate_kwargs PASSED      [  7%]
        path_to_packages/cachai/tests/test_utilities.py::test_save_func PASSED            [ 15%]
        path_to_packages/cachai/tests/test_utilities.py::test_rgb_hsl_conversions PASSED  [ 23%]
        path_to_packages/cachai/tests/test_utilities.py::test_mod_color PASSED            [ 30%]
        path_to_packages/cachai/tests/test_utilities.py::test_angspace PASSED             [ 38%]
        path_to_packages/cachai/tests/test_utilities.py::test_angdist[pi->pi] PASSED      [ 46%]
        path_to_packages/cachai/tests/test_utilities.py::test_angdist[3pi/2->pi/2] PASSED [ 53%]
        path_to_packages/cachai/tests/test_utilities.py::test_angdist[2pi->0] PASSED      [ 61%]
        path_to_packages/cachai/tests/test_utilities.py::test_quadratic_bezier PASSED     [ 69%]
        path_to_packages/cachai/tests/test_utilities.py::test_get_bezier_curve PASSED     [ 76%]
        path_to_packages/cachai/tests/test_utilities.py::test_equidistant PASSED          [ 84%]
        path_to_packages/cachai/tests/test_utilities.py::test_map_from_curve PASSED       [ 92%]
        path_to_packages/cachai/tests/test_utilities.py::test_colormapped_patch PASSED    [100%]

        ================================== 13 passed in 1.11s ==================================

    The other option is to run the tests in a Python/Jupyter file.

    .. code-block:: python
        :class: mock-block

        import cachai as ch

        # Run all tests verbose
        ch.run_tests(show_details=True)

    .. code-block:: python
        :class: mock-block

        import cachai as ch

        # Run specific tests (e.g. charts and data)
        ch.run_tests('charts','data')
    
    """
    if find_spec('pytest') is None:
        print('\nError: To run the tests you need to have pytest installed.', file=sys.stderr)
        print('You can install it with:', file=sys.stderr)
        print('\n    pip install pytest\n', file=sys.stderr)
        return None
    import pytest
    
    test_dir = Path(__file__).parent
    pytest_args = ['-p', 'no:asdf_schema_tester']
    if show_details:
        pytest_args.append('-v')

    if test_args:
        # Validation
        missing = []
        valid_tests = []
        for arg in test_args:
            test_file = test_dir / f'test_{arg}.py'
            if test_file.exists():
                valid_tests.append(str(test_file))
            else:
                missing.append(arg)
        
        if missing:
            raise ValueError(f'Tests not found: {", ".join(missing)}. '
                           f'The available tests are: {get_available_tests()}')
        
        pytest_args.extend(valid_tests)
    else:
        pytest_args.append(str(test_dir))

    plt.close('all')
    return pytest.main(pytest_args)