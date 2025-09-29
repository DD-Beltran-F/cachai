---
<p align="center">
  <img src="https://cachai.readthedocs.io/en/latest/_static/cachai_logo_wide.svg" width="500">
</p>

---

Welcome! **cachai**  (Custom Axes and CHarts Advanced Interface) is a fully customizable Python
visualization toolkit designed to deliver polished, publication-ready plots built on top of
Matplotlib. Currently, the package includes the  ``ChordDiagram``  module as its primary feature.
For details on the toolkit's capabilities, motivations and future projections, refer to
[this paper](https://iopscience.iop.org/article/10.3847/2515-5172/adf8df).

The code documentation is currently consolidated in
[Read the Docs](https://cachai.readthedocs.io/en/latest/index.html).
To contribute or report bugs, please visit the
[issues page](https://github.com/DD-Beltran-F/cachai/issues).

> **Fun fact:**
>
> "Cachai" (/kɑːˈtʃaɪ/) is a slang word from Chilean informal speech, similar to saying "ya know?"
> or "get it?" in English. Don't know how to pronounce it? Think of "kah-CHAI" (like "cut" + "chai"
> tea, with stress on "CHAI").

Please visit the following links to learn more about **cachai**:

 - [**Installation Guide**](https://cachai.readthedocs.io/en/latest/installation.html)
 - [**Getting Started**](https://cachai.readthedocs.io/en/latest/getting_started.html)
 - [**Examples**](https://cachai.readthedocs.io/en/latest/examples.html)


## **Installing cachai**

All official releases of **cachai** are published on
[:package: **PyPI**](https://pypi.org/project/cachai/). To install, simply run:

```bash
pip install cachai
```

## **Requirements**

**cachai** has been tested on  Python >= 3.10.

This Python packages are mandatory:

 - [numpy](https://numpy.org) >= 2.0.0
 - [matplotlib](https://matplotlib.org) >= 3.9.0
 - [pandas](https://pandas.pydata.org) >= 2.3.0
 - [scipy](https://scipy.org) >= 1.13.0
 - [seaborn](https://seaborn.pydata.org/index.html) >= 0.12.0

## Citing **cachai**

If **cachai** contributed to a project that resulted in a publication,
please cite [**this paper**](https://iopscience.iop.org/article/10.3847/2515-5172/adf8df).

Example citation format (``bibtex``):

```bibtex
@article{Beltrán_2025,
         doi       = {10.3847/2515-5172/adf8df},
         url       = {https://dx.doi.org/10.3847/2515-5172/adf8df},
         year      = {2025},
         month     = {aug},
         publisher = {The American Astronomical Society},
         volume    = {9},
         number    = {8},
         pages     = {216},
         author    = {Beltrán, D. and Dantas, M. L. L.},
         title     = {CACHAI’s First Module: A Fully Customizable Chord Diagram for Astronomy and Beyond},
         journal   = {Research Notes of the AAS},
}
```