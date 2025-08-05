import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.patches import Circle
from   cachai import utilities as util

@pytest.fixture
def sample_color():
    return (0.2, 0.4, 0.6)

@pytest.fixture
def sample_curve():
    return np.array([[0, 0], [1, 1], [2, 0]])

def test_validate_kwargs():
	params = {'param1': 1, 'param2': 2}
	# Test valid kwargs
	util.validate_kwargs(params, {'param1': 10})
	# Test invalid kwargs
	with pytest.raises(KeyError):
		util.validate_kwargs(params, {'invalid_param': 10})

def test_save_func(tmp_path):
    # Simple figure
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    # Testing paths
    test_dir     = tmp_path / 'tmp_images'
    test_pdf_dir = os.path.join(test_dir,'pdf')
    test_name    = 'tmp_img'
    try:
    	util.save_func(fig_name=test_name,path=test_dir,pdf=True)
    except:
    	pass
    assert os.path.exists(test_dir),\
    			'Main directory was not created'
    assert os.path.exists(test_pdf_dir),\
    			'PDF subdirectory was not created'
    assert os.path.exists(os.path.join(test_dir,f'{test_name}.png')),\
    			'PNG file was not created'
    assert os.path.exists(os.path.join(test_pdf_dir,f'{test_name}.pdf')),\
    			'PDF file was not created'
    plt.close(fig)

def test_rgb_hsl_conversions(sample_color):
    hsl = util.rgb_to_hsl(sample_color)
    rgb = util.hsl_to_rgb(hsl)
    assert np.allclose(sample_color, rgb, atol=1e-6),\
            'RGB->HSL->RGB conversion went wrong'

def test_mod_color(sample_color):
    try:
        lighter   = util.mod_color(sample_color, light=1.5)
        darker    = util.mod_color(sample_color, light=0.5)
        saturated = util.mod_color(sample_color, sat=2)
        trans     = util.mod_color(sample_color, alpha=0.5)
    except Exception as e:
        pytest.fail(f'Color was not modified correctly ({e})')
    assert np.mean(lighter) > np.mean(sample_color) > np.mean(darker),\
            'Color light was not modified correctly'
    assert np.all(saturated != sample_color),\
            'Color saturation was not modified correctly'
    assert np.all(trans != sample_color),\
            'Color transparency was not modified correctly'

def test_angspace():
    angles = util.angspace(0, np.pi/2, n=100)
    assert len(angles) == 25
    assert np.isclose(angles[-1], np.pi/2)

@pytest.mark.parametrize('inp,out', [
        (np.pi, pytest.approx(np.pi)),
        (3*np.pi/2, pytest.approx(np.pi/2)),
        (2*np.pi, pytest.approx(0)),
    ], ids=['pi->pi','3pi/2->pi/2','2pi->0'])
def test_angdist(inp,out):
    assert util.angdist(0, inp) == out

def test_quadratic_bezier(sample_curve):
    P0, P1, P2 = sample_curve
    assert np.allclose(util.quadratic_bezier(0, P0, P1, P2), P0)
    assert np.allclose(util.quadratic_bezier(1, P0, P1, P2), P2)

def test_get_bezier_curve(sample_curve):
    P0, P1, P2 = sample_curve
    curve      = util.get_bezier_curve(P0, P1, P2, n=10)
    assert curve.shape == (10, 2)
    assert np.allclose(curve[0], P0)
    assert np.allclose(curve[-1], P2)

def test_equidistant(sample_curve):
    eq_curve  = util.equidistant(sample_curve)
    diffs     = np.diff(eq_curve, axis=0)
    distances = np.linalg.norm(diffs, axis=1)
    assert np.allclose(distances, distances[0], rtol=1e-2)

def test_map_from_curve(sample_curve):
    P0, P1, P2 = sample_curve
    curve      = util.get_bezier_curve(P0, P1, P2, n=10)
    map_mat    = util.map_from_curve(curve, resolution=50)
    assert map_mat.shape == (50, 50)
    assert np.min(map_mat) >= -1
    assert np.max(map_mat) <= 1

def test_colormapped_patch(sample_curve):
    fig, ax = plt.subplots()
    patch   = Circle((0.5, 0.5), 0.4)
    ax.add_patch(patch)
    
    P0, P1, P2 = sample_curve
    curve      = util.get_bezier_curve(P0, P1, P2, n=10)
    map_mat    = util.map_from_curve(curve, resolution=50)
    img        = util.colormapped_patch(patch, map_mat, ax=ax)
    
    assert img.get_array().shape == (50, 50)
    plt.close(fig)

if __name__ == '__main__':
    pytest.main(['-v', __file__])