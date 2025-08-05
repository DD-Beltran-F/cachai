---
<p align="center">
  <img src="https://raw.githubusercontent.com/DD-Beltran-F/cachai-datasets/main/assets/cachai_logo_wide_color.svg" width="500">
</p>

---

**cachai**  (Custom Axes and CHarts Advanced Interface) is a fully customizable Python visualization toolkit designed to deliver polished, publication-ready plots built on top of Matplotlib. Currently, the package includes the  `ChordDiagram`  module as its primary feature. For details on the toolkit’s capabilities, motivations and future projections, refer to  [this paper](https://link/).

To contribute or report bugs, please visit the [issues page](https://github.com/DD-Beltran-F/cachai/issues).

# :gear: Installation guide
### **Installing cachai**

All official releases of **cachai** are published on PyPI. To install, simply run:

```bash
pip install cachai
```

If you want to verify that **cachai** works correctly on your system, you can install it with optional testing dependencies by running:

```bash
pip install cachai[testing]
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
cachai-test -v
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

If **cachai** contributed to a project that resulted in a publication, please cite [this paper](https://link/).

Example citation format:

```bibtex
@article{Beltran2025,
    author ={{Beltrán}, D. and {Dantas}, M. L. L.} ,
    title = "{CACHAI's first module: a fully customizable chord diagram for astronomy and beyond}",
    journal = {Research Notes of the American Astronomical Society},
    year = 2025,
    month = aug,
    doi = {}
}
```