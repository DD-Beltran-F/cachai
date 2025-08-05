import pytest
import matplotlib.pyplot as plt

@pytest.fixture
def figure_with_axes():
    fig, ax = plt.subplots()
    yield fig, ax
    plt.close(fig)