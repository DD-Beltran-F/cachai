import pytest
import time
import numpy as np
import matplotlib.pyplot as plt
from   cachai.chplot import chord

@pytest.fixture
def sample_corr_matrix():
    return np.array([
        [ 1.0, 0.8, -0.3],
        [ 0.8, 1.0,  0.5],
        [-0.3, 0.5,  1.0]
    ])

@pytest.fixture
def sample_names():
    return ['A', 'B', 'C']

@pytest.fixture
def sample_colors():
    return [(1,0,0), (0,1,0), (0,0,1)]  # Red, Green, Blue

@pytest.fixture
def basic_chord(figure_with_axes, sample_corr_matrix, sample_names, sample_colors):
    fig, ax = figure_with_axes
    return chord(corr_matrix=sample_corr_matrix,
        		 names=sample_names,
        		 colors=sample_colors,
        		 ax=ax)

class TestChordDiagram:
	def test_initialization(self,basic_chord):
		assert basic_chord is not None
		assert len(basic_chord.nodes) == 3

	@pytest.mark.parametrize('invalid_matrix', [
		'not_a_matrix',                   # Not a numpy array
		np.array([1, 2, 3]),              # 1D array
		np.array([[1, 2], [3, 4]]),       # Non-symmetric
		np.array([[1, 2], [2, 'a']]),     # Non-numeric values
		np.array([])                      # Empty array
		])
	def test_corr_matrices(self,invalid_matrix):
		with pytest.raises((ValueError, TypeError)):
		    chord(corr_matrix=invalid_matrix)

	def test_node_count(self,basic_chord):
		assert len(basic_chord.nodes) == basic_chord.corr_matrix.shape[0]

	def test_node_angles(self, basic_chord):
		for node in basic_chord.nodes.values():
		    assert 0 <= node['theta_i'] <= 2*np.pi
		    assert 0 <= node['theta_f'] <= 2*np.pi
		    assert node['theta_i'] < node['theta_f']
		    
	def test_scale_rho_linear(self,basic_chord):
		basic_chord.max_rho = 1.0
		basic_chord.scale   = 'linear'
		assert np.isclose(basic_chord._scale_rho(0.5), 0.5),\
				'rho = 0.5 do not satisfy the linear scale'
		assert basic_chord._scale_rho(1.0) == pytest.approx(1.0),\
				'rho = 1.0 do not satisfy the linear scale'
		assert np.isclose(basic_chord._scale_rho(-0.5), 0.5),\
				'rho = -0.5 do not satisfy the linear scale'

	def test_scale_rho_log(self,basic_chord):
		basic_chord.max_rho = 1.0
		basic_chord.scale = 'log'
		assert basic_chord._scale_rho(0.5) > 0,\
				'rho = 0.5 do not satisfy the log scale'
		assert basic_chord._scale_rho(1.0) == pytest.approx(1.0),\
				'rho = 1.0 do not satisfy the log scale'
		assert basic_chord._scale_rho(0.1) < 0.5,\
				'rho = 0.1 do not satisfy the log scale'

	@pytest.mark.parametrize('threshold,count', [(0.0,3), (0.8,2), (1.0,0)],
							 ids=['threshold=0.0','threshold=0.8','threshold=1.0'])
	def test_generation(self,sample_corr_matrix,sample_names,threshold,count):
		if threshold==1.0:
			with pytest.raises(ValueError):
				chord(corr_matrix=sample_corr_matrix,
		        	  names=sample_names,
		        	  th=threshold)
		else:
			temp_cd = chord(corr_matrix=sample_corr_matrix,
		        		 		names=sample_names,
		        		 		th=threshold)
			assert len(temp_cd.node_patches) == count,\
					'Node patches generation went wrong'
			assert len(temp_cd.node_labels)  == count,\
					'Node labels generation went wrong'
			assert sum(len(chords) for chords in temp_cd.chord_patches) >= count-1,\
					'Chord patches generation went wrong'
			assert sum(len(curves) for curves in temp_cd.bezier_curves) >= count-1,\
					'Bezier curves generation went wrong'

	def test_no_positive_correlations(self):
		cd = chord(
		    corr_matrix=np.array([
		        [1.0, -0.8, -0.5],
		        [-0.8, 1.0, -0.3],
		        [-0.5, -0.3, 1.0]
		    ]),
		    negative_hatch='///'
		)
		plt.close()
		assert cd is not None

	@pytest.mark.parametrize('size,max_time', [(15,2),(20,5),(30,10)],
							 ids=['size=15','size=20','size=30'])
	def test_large_matrix_initialization(self,size,max_time):
		# Matrix
		np.random.seed(42)
		base = np.random.rand(size, size) * 0.8 + 0.1
		large_matrix = (base + base.T) / 2
		np.fill_diagonal(large_matrix, 1.0)

		start_time = time.time()

		temp_cd = chord(corr_matrix=large_matrix,
		    			threshold=0.3,
		    			filter=False)
		initialization_time = time.time() - start_time

		assert temp_cd is not None
		assert len(temp_cd.nodes)  == size
		assert len(temp_cd.names)  == size
		assert len(temp_cd.colors) == size

		total_chords = sum(len(chords) for chords in temp_cd.chord_patches)
		expected_min_chords = size
		assert total_chords >= expected_min_chords, (
		    f'At least {expected_min_chords} connections were expected, '
		    f'but {total_chords} were found'
		)

		assert initialization_time < max_time, 'Initialization took too long'
	
	def test_large_matrix_optimization(self):
		# Matrix
		np.random.seed(42)
		size = 20
		base = np.random.rand(size, size) * 0.8 + 0.1
		large_matrix = (base + base.T) / 2
		np.fill_diagonal(large_matrix, 1.0)

		cd_no_opt = chord(corr_matrix=large_matrix,
		    			  optimize=False)
		cd_opt = chord(corr_matrix=large_matrix,
		    		   optimize=True)

		assert cd_no_opt.order != cd_opt.order,\
				'The optimization did not change the order of the nodes'
		assert set(cd_opt.order) == set(range(size)),\
				'The optimization lost some nodes'

	@pytest.mark.parametrize('node', [0,1,2],
							 ids=['node=0','node=1','node=2'])
	def test_highlighting_nodes(self,sample_corr_matrix,node):
		temp_cd = chord(corr_matrix=sample_corr_matrix,th=0)
		temp_cd.highlight_node(node)

	@pytest.mark.parametrize('node,c', [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)],
							 ids=['node=0,chord=0','node=0,chord=1',
							      'node=1,chord=0','node=1,chord=1',
							      'node=2,chord=0','node=2,chord=1'])
	def test_highlighting_chords(self,sample_corr_matrix,node,c):
		temp_cd = chord(corr_matrix=sample_corr_matrix,th=0)
		temp_cd.highlight_chord(node,c)
