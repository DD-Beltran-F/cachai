import pytest
import cachai

def test_get_dataset_repo():
	assert cachai.data.get_dataset_repo()=='https://github.com/DD-Beltran-F/cachai-datasets',\
    			'Wrong repository url'

def test_get_dataset_names():
    try:
        names = cachai.data.get_dataset_names()
    except ConnectionError:
        pytest.skip('Skipping test: network error or GitHub rate limit (429)')
    assert isinstance(names, list),\
			'Dataset names list not working'

def test_get_dataset_metadata():
    try:
        cachai.data.get_dataset_metadata('lithium')
    except ConnectionError:
        pytest.skip('Skipping test: network error or GitHub rate limit (429)')
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
            cachai.data.load_dataset(name)
    except ConnectionError:
        pytest.skip('Skipping test: network error or GitHub rate limit (429)')
    except Exception as e:
        pytest.fail(f"load_dataset went wrong when loading '{name}' ({e})")
	
def test_clear_cache():
    try:
        cachai.data.get_dataset_names()
        cachai.data.load_dataset('lithium')
    except ConnectionError:
        pytest.skip('Skipping test: network error or GitHub rate limit (429)')
	# Not-empty cache
    cachai.data.clear_cache()
    # Empty cache
    cachai.data.clear_cache()