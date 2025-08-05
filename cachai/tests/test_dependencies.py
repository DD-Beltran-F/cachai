import pytest
import importlib
from   packaging import requirements

# List of dependencies and requirements
DEPENDENCIES = [
    'matplotlib>=3.10.3',
    'numpy>=1.2.6',
    'pandas>=2.3.0',
    'seaborn>=0.13.2',
    'scipy>=1.15.3',
]

@pytest.mark.parametrize('dep', DEPENDENCIES)
def test_dependency(dep):
    req = requirements.Requirement(dep)
    try:
        mod = importlib.import_module(req.name)
        if req.specifier:
            assert req.specifier.contains(mod.__version__), \
                f'Your {req.name} version is {mod.__version__}, the requirement is {req.specifier}'
    except ImportError:
        pytest.fail(f'{req.name} is not installed')