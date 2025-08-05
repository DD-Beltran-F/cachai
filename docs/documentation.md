---
<p align="center">
  <img src="https://raw.githubusercontent.com/DD-Beltran-F/cachai-datasets/main/assets/cachai_logo_wide_color.svg" width="500">
</p>

---

**cachai**  (Custom Axes and CHarts Advanced Interface) is a fully customizable Python visualization toolkit designed to deliver polished, publication-ready plots built on top of Matplotlib. Currently, the package includes the  `ChordDiagram`  module as its primary feature. For details on the toolkit’s capabilities, motivations and future projections, refer to  [this paper](https://link/).

The code documentation and installation guide are currently consolidated in this file. To contribute or report bugs, please visit the  [GitHub repository](https://github.com/DD-Beltran-F/cachai/issues).

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

For more advanced examples, explore the Jupyter notebooks in the  [repository](https://github.com/DD-Beltran-F/cachai/tree/main/docs/notebooks).

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

# :books: Documentation

## Module structure

Currently, **cachai** has a limited set of submodules organized into 3 core functionalities: plotting, dataset access, and testing.

## Plotting with **cachai** (`cachai.chplot`)

`chplot` is the module that references all of **cachai**'s charts, providing a matplotlib-like interface for intuitive and easy plotting.

**cachai.chplot.chord**
method
```python
chplot.chord(corr_matrix,names=None,colors=None,*,**kwargs)
```
Create and return a `ChordDiagram` visualization. In science high-dimensional data are common, the choice of visualization tools directly affects both interpretation and communication. Chord diagrams are particularly valuable for illustrating weighted, non-directional connections --- such as (anti-)correlations --- between variables, treating parameters as nodes and their correlations as links.

> **Parameters:**

`corr_matrix` : `numpy.ndarray` or `pandas.DataFrame`
 - Correlation matrix for the chord diagram. This matrix has to be
   2-dimensional, not   empty, symmetric, and filled just with `int` or
   `float` values.
   
`names`/`n` : `list`
 - Names for each node (default: 'Ni' for the i-th node)
   
`colors`/`c` : `list`
 - Custom colors for nodes (default: seaborn hls palette)

> **Returns:**

`ChordDiagram`
 - An instance of the Chord Diagram class.

> **Other Parameters:**

`ax` : `matplotlib.axes.Axes`
 - Axes to plot on (default: current pyplot axis)
    
`radius`/`r` : `float`
 - Radius of the diagram (default: 1.0)
    
`position`/`p` : `list` or `tuple`
 - Position of the center of the diagram (default: (0,0))
    
`optimize` : `bool`
 - Whether to optimize node order (default: True). To optimize node ordering around the circle, we apply Prim’s algorithm (Prim, 1957), which prioritizes stronger or shorter connections to produce a visually coherent layout
    
`filter` : `bool`
 - Whether to remove nodes with no correlation (default: True)
     
`bezier_n` : `int`
 - Bezier curve resolution (default: 30)
     
`show_diag` : `bool`
 - Show self-connections (default: False)
     
`threshold`/`th` : `float`
 - Minimum correlation threshold to display (default: 0.1)
     
`node_linewidth`/`nlw` : `float`
 - Line width for nodes (default: 10)
     
`node_gap`/`ngap` : `float`
 - Gap between nodes (0 to 1) (default: 0.1)
     
`node_labelpad`/`npad` : `float`
 - Label position adjustment (default: 0.2)
     
`blend` : `bool`
 - Whether to blend chord colors (default: True)
     
`blend_resolution` : `int`
 - Color blend resolution (default: 200)
      
`chord_linewidth`/`clw` : `float`
 - Line width for chords (default: 1)
      
`chord_alpha`/`calpha` : `float`
 - Alpha of the facecolor for chords (default: 0.7)
            
`off_alpha` : `float`
 - Alpha for non-highlighted chords (default: 0.1)
            
`positive_hatch` : `str`
 - Hatch for positive correlated chords (default: None)
            
`negative_hatch` : `str`
 - Hatch for negative correlated chords (default: '---')
            
`fontsize` : `int`
 - Label font size (default: 15)
            
`font` : `dict` or `str`
 - Label font parameters (default: None)
            
`min_dist` : `float`
 - Minimum angle distance from which apply radius rule (default: 15 [degrees])
            
`scale` : `str`
 - Scale use to set chord's thickness, wheter "linear" or "log" (default: "linear")
                  
`max_rho` : `float`
 - Maximum chord's thickness (default: 0.4) 
                  
`max_rho_radius` : `float`
 - Maximum normalized radius of the chords relative to center (default: 0.7)
                  
`show_axis` : `bool`
 - Whether to show the axis (default: False)
                  
`legend` : `bool`
 - Adds default positive and negative labels in the legend (default: False)
                  
`positive_label` : `str`
 - Adds positive label in the legend (default: None)
                  
`negative_label` : `str`
 - Adds negative label in the legend (default: None)
                  
`rasterized` : `bool`
 - Whether to force rasterized (bitmap) drawing for vector graphics output (default: False)

> **Examples:**

See examples on how to use `chplot.chord` in this [Jupyter notebook](https://github.com/DD-Beltran-F/cachai/blob/main/docs/notebooks/chord_diagrams.ipynb).

Additional graphical utilities can be accessed through the `gadgets` module. Currently, the only implemented gadget is `PolarText`:

**cachai.gadgets.PolarText**
class
```python
class gadgets.PolarText(center, radius, angle, text='', pad=0.0, **kwargs):
```
Initialize a `matplotlib.text.Text` instance using polar coordinates.

> **Attributes:**

`center` : `tuple`
 - Center of the polar system in cartesian coordinates.
   
`radius` : `float`
 - Radius coordinate
   
`theta` : `float`
 - Angle coordinate in rad
   
`text` : `str`
 - Text to diplay (default: '')
    
`pad` : `float`
 - Label position adjustment (default: 0.0)
 

> **Other Attributes:**

`**kargs`
 - Attributes inherited from `matplotlib.text.Text`

> **Examples:**
```python
import matplotlib.pyplot as plt
import numnpy as np
from cachai.gadgets import PolarText

fig, ax = plt.subplots()
ax.plot([0,0],[1,1])
polar = PolarText((0,0),1,np.pi/2,text='Im polar!',pad=0.5,ha='center', va='center')
ax.add_artist(polar)
plt.show()
```

## Datasets in **cachai** (`cachai.data`)
The `data` module handles all dataset-related operations including data downloads, metadata access, and cache management.

**cachai.data.load_dataset**
method
```python
data.load_dataset(name='', redownload=False)
```
Load datasets from cachai-datasets' GitHub with a persistent cache system.

> **Parameters:**
   
`name` : `str`
 - Name of the dataset
       
`redownload` : `bool`
 - Whether to force the re-download of the dataset, ignoring cache (defaul: False)
    
> **Returns:**
       
`pandas.DataFrame`

**cachai.data.get_dataset_repo**
method
```python
data.get_dataset_repo()
```
Return the dataset repository url.

> **Returns:**
       
`str`

**cachai.data.get_dataset_names**
method
```python
data.get_dataset_names()
```
Return a list with the available datasets names.

> **Returns:**
       
`list`

**cachai.data.get_dataset_metadata**
method
```python
data.get_dataset_metadata(name)
```
Print the metadata of a specific dataset.

> **Parameters:**
   
`name` : `str`
 - Name of the dataset
       
**cachai.data.clear_cache**
method
```python
data.clear_cache(max_age_days=0)
```
Delete old cached files.

> **Parameters:**
   
`max_age_days` : `int`
 - Limit of days from which delete the cached files (e.g. `max_age_days=30` mean all the cached files older than 30 days will be deleted).
       

## Testing **cachai** (`cachai.tests`)

## Utilities (`cachai.utilities`)