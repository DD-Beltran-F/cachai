import sys
import matplotlib.pyplot as plt
from   pathlib import Path
from   importlib.util import find_spec

def run_tests(*test_args,show_details=True):
    if find_spec('pytest') is None:
        print('\nError: To run the tests you need to have pytest installed.', file=sys.stderr)
        print('You can install it with:', file=sys.stderr)
        print('\n    pip install pytest\n', file=sys.stderr)
        print('Or install cachai with the testing dependency:', file=sys.stderr)
        print('\n    pip install cachai[testing]\n', file=sys.stderr)
        return None

    import pytest
    """
    Run the tests from CACHAI.
    
    Parameters:
    -----------
    *test_args : str
        Names of the tests to run (e.g. 'charts', 'utilities').
        If not specified, all tests are run.
    show_details : bool
        Whether to add -v to the pytest command line (default: True)
    """
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

def get_available_tests():
    """Returns the list of available tests"""
    test_dir = Path(__file__).parent
    return [f.stem[5:] for f in test_dir.glob('test_*.py')]