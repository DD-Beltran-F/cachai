import pytest
import cachai
import pandas as pd

def test_get_dataset_repo():
	assert cachai.data.get_dataset_repo()=='https://github.com/DD-Beltran-F/cachai-datasets',\
    			'Wrong repository url'

def test_get_dataset_names():
	assert isinstance(cachai.data.get_dataset_names(),list),\
			'Dataset names list not working'

def test_get_dataset_metadata():
	try:
		cachai.data.get_dataset_metadata('lithium')
	except Exception as e:
		pytest.fail(f'get_dataset_metadata went wrong ({e})')

@pytest.mark.parametrize('name', ['lithium','large_correlations','invalid_name'],
					ids=["valid_name:'lithium'","valid_name:'large_correlations'",'invalid_name'])
def test_load_dataset(name):
	try:
		if name == 'invalid_name':
			with pytest.raises(ValueError):
				cachai.data.load_dataset(name)
		else:
			dataset = cachai.data.load_dataset(name)
	except Exception as e:
		pytest.fail(f"load_dataset went wrong when loading '{name}' ({e})")
	
def test_clear_cache():
	# Not-empty cache
	cachai.data.get_dataset_names()
	cachai.data.load_dataset('lithium')
	cachai.data.clear_cache()
	# Empty cache
	cachai.data.clear_cache()