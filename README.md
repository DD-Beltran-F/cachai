---
<p align="center">
  <img src="https://raw.githubusercontent.com/DD-Beltran-F/cachai/main/docs/assets/cachai_logo_wide_color.svg" width="500">
</p>

---

**cachai**  (Custom Axes and CHarts Advanced Interface) is a fully customizable Python visualization toolkit designed to deliver polished, publication-ready plots built on top of Matplotlib. Currently, the package includes the  `ChordDiagram`  module as its primary feature. For details on the toolkit’s capabilities, motivations and future projections, refer to [this paper](https://iopscience.iop.org/article/10.3847/2515-5172/adf8df).

The code documentation is currently consolidated in [docs/documentation.md](https://github.com/DD-Beltran-F/cachai/blob/main/docs/documentation.md). To contribute or report bugs, please visit the [issues page](https://github.com/DD-Beltran-F/cachai/issues).

> :cookie: **Fun fact:**
>
> "Cachai" (/kɑːˈtʃaɪ/) is a slang word from Chilean informal speech, similar to saying "ya know?" or "get it?" in English.
> Don't know how to pronounce it? Think of "kah-CHAI" (like "cut" + "chai" tea, with stress on "CHAI").

# :gear: Installation guide
### **Installing cachai**

All official releases of **cachai** are published on PyPI. To install, simply run:

```bash
pip install cachai
```

If you want to verify that **cachai** works correctly on your system, you can install it with optional testing dependencies by running:

```bash
pip install pytest
```

### **Requirements**

**cachai** has been tested on  Python >= 3.10.

**Core dependencies**: 
This Python packages are mandatory:

 - [numpy](https://numpy.org) >= 2.0.0
 - [matplotlib](https://matplotlib.org) >= 3.9.0
 - [pandas](https://pandas.pydata.org) >= 2.3.0
 - [scipy](https://scipy.org) >= 1.13.0
 - [seaborn](https://seaborn.pydata.org/index.html) >= 0.12.0

**Optional dependencies**:  
This Python packages are optional:
- [pytest](https://docs.pytest.org/en/stable/) >= 7.1.0
_(Only required for testing)_

To verify that **cachai** installed correctly and is functioning properly on your system, you can run:

```python
import cachai

cachai.run_tests()
```

Alternatively, execute this in your terminal:

```bash
cachai-test
```



# :hatching_chick: Getting started

You’ll typically need the following imports to begin using **cachai**:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cachai.chplot as chp
```

To quickly test **cachai**, you can load one of the included datasets. Currently, the available datasets are tailored for  **Chord Diagram**  use cases. Here’s a minimal example using the  `large_correlations`  dataset to generate a Chord Diagram:

```python
import cachai.data as chd
import cachai.chplot as chp

data = chd.load_dataset('large_correlations')
chp.chord(data)
```

> [!NOTE]
> Downloading datasets requires an internet connection.
>      If the files are already cached (i.e., you’ve accessed them before), **cachai** will use the local copies, allowing offline work.

For more advanced examples, explore the Jupyter notebooks in the [docs/notebooks](https://github.com/DD-Beltran-F/cachai/tree/main/docs/notebooks).

# :black_nib: Citing **cachai**

If **cachai** contributed to a project that resulted in a publication, please cite [this paper](https://iopscience.iop.org/article/10.3847/2515-5172/adf8df).

Example citation format:

```bibtex
@article{Beltrán_2025,
  doi = {10.3847/2515-5172/adf8df},
  url = {https://dx.doi.org/10.3847/2515-5172/adf8df},
  year = {2025},
  month = {aug},
  publisher = {The American Astronomical Society},
  volume = {9},
  number = {8},
  pages = {216},
  author = {Beltrán, D. and Dantas, M. L. L.},
  title = {CACHAI’s First Module: A Fully Customizable Chord Diagram for Astronomy and Beyond},
  journal = {Research Notes of the AAS},
  abstract = {We introduce ChordDiagram, the first module of Custom Axes and CHarts Advanced Interface (Cachai), a fully customizable visualization toolkit for Python. ChordDiagram creates publication-ready chord diagrams with fine control over edge styles, node colors, and layout, addressing key limitations of existing tools. Features include per-element styling, correlation thresholding, targeted highlighting, adaptive node spacing, log-scaled link thickness, and more. While broadly applicable, we showcase its use in astronomy by visualizing (anti-)correlations among stellar parameters and kinematics. ChordDiagram forms the foundation of the Cachai suite, available via pip (https://pypi.org/project/cachai), and at https://github.com/DD-Beltran-F/cachai, where the user can find a detailed documentation and examples.}
}
```