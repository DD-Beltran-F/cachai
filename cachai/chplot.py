# Basic imports
import numpy as np
from   typing import Any
from   numpy.typing import ArrayLike
from   cachai import charts
from   cachai import utilities as util
# Matplotlib imports
from   matplotlib import pyplot as plt
from   matplotlib.axes import Axes

def chord(
    corr_matrix      : np.ndarray,
    names            : ArrayLike = None,
    colors           : ArrayLike = None,
    *,
    ax               : Axes = None,
    radius           : float = 1,
    position         : ArrayLike = (0,0),
    optimize         : bool = True,
    filter           : bool = True,
    bezier_n         : int = 30,
    show_diag        : bool = False,
    threshold        : float = 0.1,
    node_linewidth   : float = 10,
    node_gap         : float = 0.1,
    node_labelpad    : float = 0.2,
    blend            : bool = True,
    blend_resolution : int = 200,
    chord_linewidth  : float = 1,
    chord_alpha      : float = 0.7,
    positive_hatch   : str = None,
    negative_hatch   : str = '---',
    fontsize         : int = 15,
    font             : dict | str = None,
    min_dist         : float = np.deg2rad(15),
    scale            : str = 'linear',
    max_rho          : float = 0.4,
    max_rho_radius   : float = 0.7,
    show_axis        : bool = False,
    legend           : bool = False,
    positive_label   : str = None,
    negative_label   : str = None,
    rasterized       : bool = False,
    **kwargs         : Any,
    ) -> charts.ChordDiagram:
    """
    Create and return a ChordDiagram visualization.
    
    Parameters:
    -----------
    corr_matrix : ndarray
        Correlation matrix for the chord diagram
    names / n : list
        Names for each node (default: 'Ni' for the i-th node)
    colors / c : list
        Custom colors for nodes (default: seaborn hls palette)
    ax : matplotlib.axes.Axes
        Axes to plot on (default: current pyplot axis)
    radius / r : float
        Radius of the diagram (default: 1.0)
    position / p : tuple
        Position of the center of the diagram (default: (0,0))
    optimize : bool
        Whether to optimize node order (default: True)
    filter : bool
        Whether to remove nodes with no correlation (default: True)
    bezier_n : int
        Bezier curve resolution (default: 30)
    show_diag : bool
        Show self-connections (default: False)
    threshold / th : float
        Minimum correlation threshold to display (default: 0.1)
    node_linewidth / nlw : float
        Line width for nodes (default: 10)
    node_gap / ngap : float
        Gap between nodes (0-1) (default: 0.1)
    node_labelpad / npad : float
        Label position adjustment (default: 0.2)
    blend : bool
        Whether to blend chord colors (default: False)
    blend_resolution : int
        Color blend resolution (default: 200)
    chord_linewidth / clw : float
        Line width for chords (default: 1)
    chord_alpha / calpha : float
        Alpha of the facecolor for chords (default: 0.7)
    positive_hatch : str
        Hatch for positive correlated chords (default: None)
    negative_hatch : str
        Hatch for negative correlated chords (default: '---')
    fontsize : int
        Label font size (default: 15)
    font : dict or str
        Label font parameters (default: None)
    min_dist : float
        Minimum angle distance from which apply radius rule (default: 15 [degrees])
    scale : str
        Scale use to set chord's thickness, wheter "linear" or "log" (default: "linear")
    max_rho : float
        Maximum chord's thickness (default: 0.4) 
    max_rho_radius : float
        Maximum normalized radius of the chords relative to center (default: 0.7)
    show_axis : bool
        Whether to show the axis (default: False)
    legend : bool
        Adds default positive and negative labels in the legend (default: False)
    positive_label : str
        Adds positive label in the legend (default: None)
    negative_label : str
        Adds negative label in the legend (default: None)
    rasterized : bool
        Whether to force rasterized (bitmap) drawing for vector graphics output (default: False)
    
    Returns:
    --------
    ChordDiagram
        An instance of the ChordDiagram class
    """
    # Process parameters
    params = {
        'corr_matrix'      : corr_matrix,
        'names'            : names,
        'colors'           : colors,
        'ax'               : ax if ax is not None else plt.gca(),
        'radius'           : radius,
        'position'         : position,
        'optimize'         : optimize,
        'filter'           : filter,
        'bezier_n'         : bezier_n,
        'show_diag'        : show_diag,
        'threshold'        : threshold,
        'node_linewidth'   : node_linewidth,
        'node_gap'         : node_gap,
        'node_labelpad'    : node_labelpad,
        'blend'            : blend,
        'blend_resolution' : blend_resolution,
        'chord_linewidth'  : chord_linewidth,
        'chord_alpha'      : chord_alpha,
        'positive_hatch'   : positive_hatch,
        'negative_hatch'   : negative_hatch,
        'fontsize'         : fontsize,
        'font'             : font,
        'min_dist'         : min_dist,
        'scale'            : scale,
        'max_rho'          : max_rho,
        'max_rho_radius'   : max_rho_radius,
        'show_axis'        : show_axis,
        'legend'           : legend,
        'positive_label'   : positive_label,
        'negative_label'   : negative_label,
        'rasterized'       : rasterized,
    }
    
    # Alternative kwargs aliases
    aliases = {'names'           : 'n',
               'colors'          : 'c',
               'radius'          : 'r',
               'position'        : 'p',
               'threshold'       : 'th',
               'node_linewidth'  : 'nlw',
               'node_gap'        : 'ngap',
               'node_labelpad'   : 'npad',
               'chord_linewidth' : 'clw',
               'chord_alpha'     : 'calpha'
              }
    
    for key in aliases:
        if aliases[key] in kwargs: params[key] = kwargs.pop(aliases[key])

    # Check for wrong kwargs
    util.validate_kwargs(params,kwargs,aliases)

    return charts.ChordDiagram(**params)

    