# Basic imports
import numpy as np
from   matplotlib import pyplot as plt
# Cachai imports
from   cachai._core.chord import ChordDiagram
from   cachai.gadgets import PolarText
from   cachai.utilities import validate_kwargs

def chord(
        corr_matrix,names=None,colors=None,*,ax=None,radius=1,position=(0,0),optimize=True,
        filter=True,bezier_n=30,show_diag=False,threshold=0.1,node_linewidth=10,node_gap=0.1,
        node_labelpad=0.2,blend=True,blend_resolution=200,chord_linewidth=1,chord_alpha=0.7,
        off_alpha=0.1,positive_hatch=None,negative_hatch='---',fontsize=15,font=None,
        min_dist=np.deg2rad(15),scale='linear',max_rho=0.4,max_rho_radius=0.7,show_axis=False,
        legend=False,positive_label=None,negative_label=None,rasterized=False,**kwargs,
    ):
    """
    A Chord Diagram from a correlation matrix, with customizable threshold, style, and colors.
    
    In science, high-dimensional data are common, the choice of visualization tools directly affects
    both interpretation and communication. Chord diagrams are particularly valuable for illustrating
    weighted, non-directional connections --- such as (anti-)correlations --- between variables,
    treating parameters as nodes and their correlations as links.

        
    Parameters
        corr_matrix : :class:`numpy.ndarray` or :class:`pandas.DataFrame`
            Correlation matrix for the chord diagram. This matrix has to be 2-dimensional, not
            empty, symmetric, and filled just with ``int`` or ``float`` values.
        names / n : :class:`list`, optional
            Names for each node (default: 'Ni' for the i-th node)
        colors / c : :class:`list`, optional
            Custom colors for nodes (default: seaborn hls palette)
        ax : :class:`matplotlib.axes.Axes`, optional
            Axes to plot on (default: current pyplot axis)
    
    Returns
        :class:`ChordDiagram`:viewsource:`cachai._core.chord.ChordDiagram`
            An instance of the ChordDiagram class

    Other Parameters
        radius / r : :class:`float`
            Radius of the diagram (default: 1.0)
        position / p : :class:`tuple`
            Position of the center of the diagram (default: (0,0))
        optimize : :class:`bool`
            Whether to optimize node order (default: True)
        filter : :class:`bool`
            Whether to remove nodes with no correlation (default: True)
        bezier_n : :class:`int`
            Bezier curve resolution (default: 30)
        show_diag : :class:`bool`
            Show self-connections (default: False)
        threshold / th : :class:`float`
            Minimum correlation threshold to display (default: 0.1)
        node_linewidth / nlw : :class:`float`
            Line width for nodes (default: 10)
        node_gap / ngap : :class:`float`
            Gap between nodes (0-1) (default: 0.1)
        node_labelpad / npad : :class:`float`
            Label position adjustment (default: 0.2)
        blend : :class:`bool`
            Whether to blend chord colors (default: True)
        blend_resolution : :class:`int`
            Color blend resolution (default: 200)
        chord_linewidth / clw : :class:`float`
            Line width for chords (default: 1)
        chord_alpha / calpha : :class:`float`
            Alpha of the facecolor for chords (default: 0.7)
        off_alpha : :class:`float`
            Alpha for non-highlighted chords (default: 0.1)
        positive_hatch : :class:`str`
            Hatch for positive correlated chords (default: None)
        negative_hatch : :class:`str`
            Hatch for negative correlated chords (default: '---')
        fontsize : :class:`int`
            Label font size (default: 15)
        font : :class:`dict` or :class:`str`
            Label font parameters (default: None)
        min_dist : :class:`float`
            Minimum angle distance from which apply radius rule (default: 15 [degrees])
        scale : :class:`str`
            Scale use to set chord's thickness, wheter "linear" or "log" (default: "linear")
        max_rho : :class:`float`
            Maximum chord's thickness (default: 0.4) 
        max_rho_radius : :class:`float`
            Maximum normalized radius of the chords relative to center (default: 0.7)
        show_axis : :class:`bool`
            Whether to show the axis (default: False)
        legend : :class:`bool`
            Adds default positive and negative labels in the legend (default: False)
        positive_label : :class:`str`
            Adds positive label in the legend (default: None)
        negative_label : :class:`str`
            Adds negative label in the legend (default: None)
        rasterized : :class:`bool`
            Whether to force rasterized (bitmap) drawing for vector graphics output (default: False)
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    First, import **cachai** and the necessary libraries.
    
    .. code-block:: python
        :class: mock-block

        import matplotlib.pyplot as plt
        import cachai.chplot as chp


    The only mandatory parameter for ``chord()`` is the correlation matrix. Assuming you already
    have your matrix, this line will show the default plot (in some IDLEs you need to
    add ``plt.show()``):

    .. code-block:: python
        :class: mock-block

        chp.chord(corr_matrix)
        

    Now, if you want to add a legend distinguishing positive and negative correlations, just set
    ``legend=True``. Check the next example:

    .. code-block:: python
        :class: mock-block

        plt.figure(figsize=(6,6))

        chp.chord(corr_matrix,
                  threshold=0.3,
                  negative_hatch='///',
                  legend=True,
                  rasterized=True)

        plt.legend(loc='center',bbox_to_anchor=[0.5,0],ncols=2,fontsize=13,handletextpad=0)
        plt.show()

    To see more examples on how to use ``chplot.chord()`` check out the
    :doc:`examples section <../../examples>`.


    Methods
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. currentmodule:: cachai._core.chord

    .. automethod:: ChordDiagram.highlight_node
        :noindex:
    .. automethod:: ChordDiagram.highlight_chord
        :noindex:
    .. automethod:: ChordDiagram.set_chord_alpha
        :noindex:
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
        'off_alpha'        : off_alpha,
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
    validate_kwargs(kwargs.keys(),params.keys(),aliases)

    return ChordDiagram(**params)

def polartext(radius,angle,text,center=(0,0),pad=0.0,**kwargs):
    """
    Place text at specified polar coordinates relative to a center point.

    Parameters
        radius : :class:`float`
            Radius coordinate from the center.
        theta : :class:`float`
            Angle in degrees (0° at positive x-axis, increasing counterclockwise).
        text : :class:`str`
            Text to diplay.
        center : :class:`tuple`, optional
            Center coordinates (x,y) (default: (0,0)).
        pad : :class:`float`, optional
            Padding value (positive for outward displacement, negative for inward).
    
    Returns
        :class:`PolarText`:viewsource:`cachai.gadgets.PolarText`
            An instance of Polar Text (base: :class:`matplotlib.text.Text`)

    Other Parameters
        ``**kwargs``
            Keyword arguments of :class:`matplotlib.text.Text`.
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: mock-block

        import matplotlib.pyplot as plt
        import cachai.chplot as chp

        fig, ax = plt.subplots()
        ax.plot([0,0],[1,1])
        chp.polartext((0,0),1,45,text='Im polar!',pad=0.5,ha='center',va='center')
        plt.show()

    To see more examples check out the :doc:`examples section <../../examples>`.

    Methods
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. currentmodule:: cachai.gadgets

    .. automethod:: PolarText.set_polar_position
        :noindex:
    .. automethod:: PolarText.set_pad
        :noindex:
    .. automethod:: PolarText.set_radius
        :noindex:
    .. automethod:: PolarText.set_angle
        :noindex:
    .. automethod:: PolarText.set_center
        :noindex:
    
    Other Methods
        Inherited from :class:`matplotlib.text.Text`.
    """
    ax     = plt.gca()
    artist = PolarText(radius,angle,text,center,pad,**kwargs)
    ax.add_artist(artist)
    return artist