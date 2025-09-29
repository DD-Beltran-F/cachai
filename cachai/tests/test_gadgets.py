import pytest
import numpy as np
from   matplotlib.text import Text
from   cachai.gadgets import PolarText

@pytest.fixture
def sample_polartext():
    return PolarText(center=(0, 0), radius=1, angle=45, text="Test", pad=0.1)

class TestPolarText:
    def test_inheritance(self,sample_polartext):
        assert isinstance(sample_polartext, Text),\
                'PolarText do not inherit from matplotlib.text.Text'

    def test_cartesian_coords(self,sample_polartext):
        expected_x = (1 + 0.1) * np.cos(np.pi/4)
        expected_y = (1 + 0.1) * np.sin(np.pi/4)
        actual_x, actual_y = sample_polartext.get_position()
        assert np.isclose(actual_x, expected_x)
        assert np.isclose(actual_y, expected_y)

    def test_properties_set(self,sample_polartext):
        """Verifica que las propiedades se establecen correctamente"""
        test_pt = PolarText(sample_polartext.center, sample_polartext._radius,
                            sample_polartext._angle,text='Test text')
        test_pt.set_polar_position(radius=2.5,angle_deg=25,center=(3,4))
        assert np.array_equal(test_pt.center, np.array([3, 4]))
        assert test_pt._radius == 2.5
        assert np.isclose(test_pt._angle, np.deg2rad(25))
        test_pt.set_pad(0.5)
        assert test_pt._pad == 0.5
        assert test_pt.get_text() == 'Test text'

    def test_add_to_axes(self,figure_with_axes,sample_polartext):
        fig, ax = figure_with_axes
        ax.add_artist(sample_polartext)
        assert sample_polartext in ax.texts,\
                'PolarText is not in the artists list'

    def test_rendering(self,figure_with_axes):
        fig, ax = figure_with_axes
        try:
            texts = [PolarText((0, 0), 1, 0, '0°'),
                     PolarText((0, 0), 1, 90, '90°'),
                     PolarText((0, 0), 1, 180, '180°', pad=0.2)]
            for text in texts:
                ax.add_artist(text)
            fig.canvas.draw()
        except Exception as e:
            pytest.fail(f'PolarText rendering went wrong ({e})')

if __name__ == '__main__':
    pytest.main(['-v', __file__])