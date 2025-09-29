import sys
import argparse
from cachai.tests._run_test import run_tests

def main():
    parser = argparse.ArgumentParser(
        description='Run the tests from CACHAI',
        usage='%(prog)s [OPTIONS] [TESTS...]'
    )
    
    # For specific tests
    parser.add_argument(
        'tests',
        nargs='*',
        default=[],
        help="Names of the tests to run (e.g. 'charts', 'utilities'). If not specified, all tests are run."
    )
    
    # Option to show details
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output (equivalent to pytest -v)'
    )
    
    # Option to show available tests
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all available tests without running them'
    )
    
    args = parser.parse_args()
    
    if args.list:
        from cachai.tests._run_test import get_available_tests
        print('Available tests:')
        for test in get_available_tests():
            print(f'  {test}')
        sys.exit(0)
    
    sys.exit(run_tests(*args.tests))

if __name__ == '__main__':
    main()