# Imports
import os
import numpy as np
import colorsys
# Matplotlib imports
from   matplotlib import pyplot as plt
# Scipy imports
from   scipy.spatial.distance import cdist
from   scipy.interpolate import interp1d

def chsave(name="figure",dir_path="images",pdf=True,img_dpi=300,pdf_dpi=200):
    """
    Saves the current matplotlib figure as PNG and optionally PDF with customizable *dpi*
    (dots per inch).

    Parameters
        name : :class:`str`
            The name of the figure. The image is saved as "dir_path/name.png" (default: "figure").
    
    Other Parameters
        dir_path : :class:`str`
            Path to the directory where the image is saved. If it doesn't exist, it will be created
            (default: "images")
        pdf : :class:`bool`
            Whether to also save the image as a PDF.
        img_dpi : :class:`int`
            The *dpi* of the PNG image.
        pdf_dpi : :class:`int`
            The *dpi* of the PDF image.
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: mock-block

        import cachai.utilities as chu

        plt.figure(figsize=(10,10))
        plt.scatter([1,2,3],[1,4,9],color="magenta")

        chu.chsave("my_plot")
    """
    if not os.path.exists(dir_path): os.makedirs(dir_path)
    plt.savefig(os.path.join(dir_path,f'{name}.png'),
                bbox_inches='tight',pad_inches=0.3,dpi=img_dpi)
    if pdf:
        if not os.path.exists(os.path.join(dir_path,'pdf')):
            os.makedirs(os.path.join(dir_path,'pdf'))
        plt.savefig(os.path.join(dir_path,'pdf',f'{name}.pdf'),
                    bbox_inches='tight',pad_inches=0.3,dpi=pdf_dpi)

def angdist(alpha,beta):
    """
    Calculates the minimal angular distance between two angles in radians.

    Parameters
        alpha : :class:`float`
            Angle in radians.
        beta : :class:`float`
            Angle in radians.
    
    Returns
        :class:`float`

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import numpy as np

        A = np.pi/4
        B = 3*np.pi/4
        
        distance = chu.angdist(A,B)

        print("Distance in radians:",distance)
        print("Distance in degrees:",np.rad2deg(distance))
    
    .. code-block:: text
        :class: out-block

        Distance in radians: 1.5707963267948966
        Distance in degrees: 90.0
    """
    diff = np.abs(alpha - beta) % (2 * np.pi)
    return np.min([diff, 2 * np.pi - diff])

def _angspace(alpha,beta,n=200):
    """:meta-private:
    Generate a linear space of angles
    """
    theta = abs(beta-alpha)
    ndots = int(theta*n/(2*np.pi))
    if ndots == 1: ndots = 2
    return np.linspace(alpha,beta,ndots)

def map_from_curve(curve=None,xlim=(-1,1),ylim=(-1,1),resolution=200):
    """
    Generates a map (2D matrix) where each point value is based on its proximity to the nearest
    point along a specified curve.

    Parameters
        curve : :class:`numpy.ndarray`
            1D array of points (x,y) defining the reference curve.
        xlim : :class:`tuple` or :class:`array-like`, optional
            x-axis boundaries of the map.
        ylim : :class:`tuple` or :class:`array-like`, optional
            y-axis boundaries of the map.
        resolution : :class:`int`, optional
            Number of grid points along each axis for the output map.
    
    Returns
        :class:`numpy.ndarray` : 2D array

        or

        :class:`None` : If ``curve = None``

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import numpy as np

        # Constructing a sine curve
        x_array = np.linspace(0,2*np.pi,500)
        y_array = np.sin(x_array)
        curve   = np.array([(x,y) for x,y in zip(x_array,y_array)])

        my_map = chu.map_from_curve(curve,xlim=(0,2*np.pi),ylim=(-1,1),resolution=5)

        print(my_map)
    
    .. code-block:: text
        :class: out-block

        [[-1.         -0.10220441  0.15430862  0.498998    0.84769539]
         [-1.         -0.77955912  0.07815631  0.498998    0.91983968]
         [-1.         -0.498998    0.00200401  0.498998    1.        ]
         [-0.91983968 -0.498998   -0.07815631  0.77955912  1.        ]
         [-0.84769539 -0.498998   -0.15430862  0.10220441  1.        ]]
    """
    if curve is None: return None
    
    # Values from curve
    values = np.linspace(-1,1,len(curve))
    
    # Mesh
    x = np.linspace(*xlim, resolution)
    y = np.linspace(*ylim, resolution)
    grid_x, grid_y = np.meshgrid(x, y, indexing='xy')
    grid_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))

    # Obtain the nearest point in the curve and use that value
    distances             = cdist(grid_points, curve)
    nearest_point_indexes = np.argmin(distances, axis=1)
    map_flat              = values[nearest_point_indexes]
    map_matrix            = map_flat.reshape(resolution, resolution)
    
    return map_matrix

def colormapped_patch(patch,map_matrix,ax=None,colormap="coolwarm",
                      zorder=5,alpha=0.5,rasterized=False):
    """
    Applies a colormap to a patch object using a precomputed map matrix, creating a color-filled
    shape.

    Parameters
        patch : :class:`matplotlib.patches.Patch` and similar
            Matplotlib patch object to be filled with colors.
        map_matrix : :class:`numpy.ndarray`
            2D array containing color values for the mapping.
            
    Returns
        :class:`matplotlib.image.AxesImage`

    Other Parameters
        ax : :class:`matplotlib.axes.Axes`
            Axes object where the patch will be drawn (default: current axes).
        colormap : :class:`str` or :class:`matplotlib.colors.LinearSegmentedColormap`
            Matplotlib colormap to use.
        zorder : :class:`int`
            Rendering order layer for the patch.
        alpha : :class:`float`
            Transparency level of the filled patch.
        rasterized : :class:`bool`
            Whether to rasterize the patch for better performance.

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: mock-block

        import cachai.utilities as chu
        import numpy as np
        import matplotlib.pyplot as plt
        from   matplotlib.patches import Circle

        # Create a circular patch
        circle = Circle((0.5, 0.5), 0.3)
        # Generate a simple gradient map
        gradient = np.linspace(-1, 1, 400).reshape(20, 20)

        fig, ax = plt.subplots()
        ax.add_patch(circle)
        chu.colormapped_patch(circle, gradient, ax=ax)
        plt.show()
    """
    if ax is None: ax = plt.gca()
    
    vertices   = patch.get_path().vertices
    xmin, ymin = np.min(vertices, axis=0)
    xmax, ymax = np.max(vertices, axis=0)
    
    img = ax.imshow(
        map_matrix, 
        cmap=colormap, 
        extent=(xmin, xmax, ymin, ymax), 
        origin='lower',
        aspect='auto',
        clip_path=patch,
        clip_on=True,
        zorder=zorder,
        alpha=alpha,
        rasterized=rasterized,
        vmin=-1, vmax=1
    )
    return img

def equidistant(points):
    """
    Resamples points along a curve to make them equidistant while preserving the overall shape.

    Parameters
        points : :class:`numpy.ndarray`
            1D array of points (x,y) defining the reference curve.
    
    Returns
        :class:`numpy.ndarray` : 2D array
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import numpy as np

        # Create a non-uniform curve
        original_points = np.array([[0, 0], [1, 2], [3, 1], [4, 4]])

        # Make points equidistant
        equal_points = chu.equidistant(original_points)

        print(equal_points)
        
    .. code-block:: python
        :class: out-block

        [[0.         0.        ]
         [1.27614237 1.86192881]
         [3.19526215 1.58578644]
         [4.         4.        ]]
    """
    # Cumulative distances between consecutive points
    diffs             = np.diff(points, axis=0)
    distances         = np.linalg.norm(diffs, axis=1)
    cumulative_length = np.insert(np.cumsum(distances), 0, 0)

    # Interpolation
    total_length  = cumulative_length[-1]
    new_distances = np.linspace(0, total_length, len(points))

    interp_x = interp1d(cumulative_length, points[:, 0], kind='linear')
    interp_y = interp1d(cumulative_length, points[:, 1], kind='linear')
    
    # Equidistant curve
    new_x = interp_x(new_distances)
    new_y = interp_y(new_distances)
    
    return np.column_stack((new_x, new_y))

def quadratic_bezier(t,P0,P1,P2):
    """
    Evaluates a
    `quadratic Bézier <https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_curves>`_ curve
    at parameter ``t`` using three control points.

    Parameters
        t : :class:`float`
            Parameter value between 0.0 and 1.0.
        P0 : :class:`tuple` or :class:`array-like`
            Starting control point (x,y).
        P1 : :class:`tuple` or :class:`array-like`
            Middle control point (x,y).
        P2 : :class:`tuple` or :class:`array-like`
            Ending control point (x,y).
    
    Returns
        :class:`numpy.ndarray` : point (x,y)
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        
        # Evaluate curve at midpoint
        point = chu.quadratic_bezier(0.5, (0, 0), (1, 2), (3, 1))

        print(point)
        
    .. code-block:: python
        :class: out-block

        [1.25 1.25]
    """
    if (P0 is None) or (P1 is None) or (P2 is None): return None
    P0 = np.array(P0); P1 = np.array(P1); P2 = np.array(P2)
    return (1-t)**2 * P0 + 2*(1-t)*t * P1 + t**2 * P2

def get_bezier_curve(P0,P1,P2,n=20):
    """
    Generates a sequence of points along a
    `quadratic Bézier curve <https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_curves>`_.

    Parameters
        P0 : :class:`tuple` or :class:`array-like`
            Starting control point (x,y).
        P1 : :class:`tuple` or :class:`array-like`
            Middle control point (x,y).
        P2 : :class:`tuple` or :class:`array-like`
            Ending control point (x,y).
        n : :class:`int`
            Number of points to generate along the curve (default: 20).
    
    Returns
        :class:`numpy.ndarray` : 1D array of points (x,y)
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        
        curve = chu.get_bezier_curve([0, 0], [2, 3], [4, 1], n=10)

        print(curve)
        
    .. code-block:: python
        :class: out-block

        [[0.         0.        ]
         [0.44444444 0.60493827]
         [0.88888889 1.08641975]
         [1.33333333 1.44444444]
         [1.77777778 1.67901235]
         [2.22222222 1.79012346]
         [2.66666667 1.77777778]
         [3.11111111 1.64197531]
         [3.55555556 1.38271605]
         [4.         1.        ]]
    """
    if (P0 is None) or (P1 is None) or (P2 is None): return None
    t_values = np.linspace(0, 1, n)
    return np.array([quadratic_bezier(t, P0, P1, P2) for t in t_values])

def validate_kwargs(keys,allowed_keys,aliases={}):
    """
    Validates that given keyword arguments are within the allowed set of parameters.
    
    Parameters
        keys : :class:`list` or :class:`array-like`
            A list with the name of the key arguments you want to validate.
        allowed_keys : :class:`list` or :class:`array-like`
            A list with the name of the valid arguments.
        aliases : :class:`dict`, optional
            A python dictionary with alternative aliases for the key arguments ().

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu

        user_given_kwargs = {'name': 'Agustina', 'favorite_artist': 'Chappell Roan'}

        allowed_params  = ['name', 'age', 'favorite_color']
        aliases         = {'favorite_color': 'favc'}

        chu.validate_kwargs(user_given_kwargs.keys(),allowed_params,aliases)
    
    .. code-block:: python-console
        :class: out-block

        ---------------------------------------------------------------------------
        Traceback (most recent call last):
            line 8
        KeyError: 'Invalid argument "favorite_artist". Allowed arguments are: name, age, favorite_color / favc.'
    """
    for key in keys:
        if key not in allowed_keys:
            raise KeyError(
            f'Invalid argument "{key}". Allowed arguments are: '
            f'{kwargs_as_string(allowed_keys,aliases)}.'
            )

def kwargs_as_string(keys,aliases={}):
    """
    Formats keyword argument names as a readable string separated by ``,``, with optional aliases.

    Parameters
        keys : :class:`list` or :class:`array-like`
            A list with the name of the key arguments you want to format as string.
        aliases : :class:`dict`, optional
            A python dictionary with alternative aliases for the key arguments ().
    
    Returns
        :class:`str`

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu

        params  = {'name': 'Fabian', 'age': 21, 'favorite_color': 'blue'}
        aliases = {'favorite_color': 'favc'}

        my_kwargs = chu.kwargs_as_string(params.keys(),aliases)
        
        print(f"The arguments of my function are {my_kwargs}.")
    
    .. code-block:: text
        :class: out-block
        
        "The arguments of my function are name, age, favorite_color / favc."
    """
    if not isinstance(keys,list): keys = list(keys)
    for i,key in enumerate(keys):
        if key in aliases.keys(): keys[i] = f'{key} / {aliases[key]}'
    return ', '.join(keys)

def mod_color(color,light=1.0,sat=1.0,alpha=1.0,alpha_bg=(1.0,1.0,1.0)):
    """
    Applies multiple color modifications (lightness, saturation, transparency) to an RGB color.
    
    Parameters
        color : :class:`tuple` or :class:`array-like`
            Triplet with the three RGB values (in arithmetic notation, i.e. 0.0 to 1.0)
        light : :class:`float`
            Lightness factor. 1.0 means no change.
        sat : :class:`float`
            Saturation factor. 1.0 means no change.
        alpha : :class:`float`
            Transparency level (0.0 to 1.0).
        alpha_bg : :class:`tuple` or :class:`array-like`
            Background color. Since transparency isn't actually achieved, a background color is set.
            The color is combined with the background color. Default is white.
    
    Returns
        :class:`tuple` : RGB color
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import matplotlib.colors as mcolors

        # matplotlib.colors.to_rgb also supports HEX codes
        my_color = mcolors.to_rgb("violet")

        # Make it 50% darker, saturate to 150% and set the transparency to 30%
        new_color = chu.mod_color(my_color,light=0.5,sat=1.5,alpha=0.3)

        print("my_color:",my_color)
        print("new_color:",new_color)
    
    .. code-block:: text
        :class: out-block
        
        my_color: (0.9333333333333333, 0.5098039215686274, 0.9333333333333333)
        new_color: (0.8558823529411764, 0.7605882352941176, 0.8558823529411764)
    """
    new_color = color
    # Light
    if light > 1:
        new_color = brighter_color(new_color,factor=light-1)
    elif light < 1:
        new_color = darker_color(new_color,factor=1-light)
    # Saturation
    new_color = saturate_color(new_color,factor=sat)
    # Alpgha
    new_color = alpha_color(new_color,alpha=alpha,bg=alpha_bg)
    return new_color

def brighter_color(color,factor=0.0):
    """
    Increases the brightness of an RGB color by a specified factor.
    
    Parameters
        color : :class:`tuple` or :class:`array-like`
            Triplet with the three RGB values (in arithmetic notation, i.e. 0.0 to 1.0)
        factor : :class:`float`
            Brightness factor. 0.0 means no change.
    
    Returns
        :class:`tuple` : RGB color
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import matplotlib.colors as mcolors

        # matplotlib.colors.to_rgb also supports HEX codes
        my_color = mcolors.to_rgb("violet")

        # Make it 50% brighter
        new_color = chu.brighter_color(my_color,factor=0.5)

        print("my_color:",my_color)
        print("new_color:",new_color)
    
    .. code-block:: text
        :class: out-block
        
        my_color: (0.9333333333333333, 0.5098039215686274, 0.9333333333333333)
        new_color: (0.9666666666666667, 0.7549019607843137, 0.9666666666666667)
    """
    r,g,b = color
    factor = max(0, factor)
    r = min(1, r + (1-r)*factor)
    g = min(1, g + (1-g)*factor)
    b = min(1, b + (1-b)*factor)
    return (r,g,b)

def darker_color(color,factor=0.0):
    """
    Decreases the brightness of an RGB color by a specified factor.
    
    Parameters
        color : :class:`tuple` or :class:`array-like`
            Triplet with the three RGB values (in arithmetic notation, i.e. 0.0 to 1.0)
        factor : :class:`float`
            Darkness factor. 0.0 means no change.
    
    Returns
        :class:`tuple` : RGB color
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import matplotlib.colors as mcolors

        # matplotlib.colors.to_rgb also supports HEX codes
        my_color = mcolors.to_rgb("violet")

        # Make it 50% darker
        new_color = chu.darker_color(my_color,factor=0.5)

        print("my_color:",my_color)
        print("new_color:",new_color)
    
    .. code-block:: text
        :class: out-block
        
        my_color: (0.9333333333333333, 0.5098039215686274, 0.9333333333333333)
        new_color: (0.4666666666666667, 0.2549019607843137, 0.4666666666666667)
    """
    r,g,b = color
    factor = 1 - (max(0,factor))
    r = max(0, r*factor)
    g = max(0, g*factor)
    b = max(0, b*factor)
    return (r,g,b)

def saturate_color(color,factor=1.0):
    """
    Adjusts the saturation level of an RGB color by a specified factor.
    
    Parameters
        color : :class:`tuple` or :class:`array-like`
            Triplet with the three RGB values (in arithmetic notation, i.e. 0.0 to 1.0)
        factor : :class:`float`
            Saturation factor. 1.0 means no change.
    
    Returns
        :class:`tuple` : RGB color
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import matplotlib.colors as mcolors

        # matplotlib.colors.to_rgb also supports HEX codes
        my_color = mcolors.to_rgb("violet")

        # Saturate to 150%
        new_color = chu.saturate_color(my_color,factor=1.5)

        print("my_color:",my_color)
        print("new_color:",new_color)
    
    .. code-block:: text
        :class: out-block
        
        my_color: (0.9333333333333333, 0.5098039215686274, 0.9333333333333333)
        new_color: (1.0, 0.44313725490196076, 0.9999999999999999)
    """
    r,g,b = color
    h,l,s = colorsys.rgb_to_hls(r,g,b)
    s_new = max(0, min(1,s*factor))
    r,g,b = colorsys.hls_to_rgb(h,l,s_new)
    return (r,g,b)

def alpha_color(color, alpha=1.0, bg=(1.0,1.0,1.0)):
    """
    Simulates transparency by blending an RGB color with a background color.
    
    Parameters
        color : :class:`tuple` or :class:`array-like`
            Triplet with the three RGB values (in arithmetic notation, i.e. 0.0 to 1.0)
        alpha : :class:`float`
            Transparency level (0.0 to 1.0).
        bg : :class:`tuple` or :class:`array-like`
            Background color. Since transparency isn't actually achieved, a background color is set.
            The color is combined with the background color. Default is white.
    
    Returns
        :class:`tuple` : RGB color
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu
        import matplotlib.colors as mcolors

        # matplotlib.colors.to_rgb also supports HEX codes
        my_color = mcolors.to_rgb("violet")

        # Set the transparency to 30%
        new_color = chu.alpha_color(my_color,alpha=0.3)

        print("my_color:",my_color)
        print("new_color:",new_color)
    
    .. code-block:: text
        :class: out-block
        
        my_color: (0.9333333333333333, 0.5098039215686274, 0.9333333333333333)
        new_color: (0.98, 0.8529411764705882, 0.98)
    """
    r,g,b = color
    bg_r,bg_g,bg_b = bg
    factor = max(0, min(1, alpha))
    r_result = (r*factor) + (bg_r*(1-factor))
    g_result = (g*factor) + (bg_g*(1-factor))
    b_result = (b*factor) + (bg_b*(1-factor))
    return (r_result,g_result,b_result)

# f-string pre-defined colors
_fstr_colors = {'white':255,'black':232,'light_gray':245,'dark_gray':237,'gold':220,
               'red':196,'blue':21,'green':118,'magenta':165,'mint':87,'orange':202}

def strcol(string,c="white"):
    """
    Applies ANSI color codes to a string (only work in terminal/output cells).
    
    Parameters
        string : :class:`str`
            The string you want to color.
        c : :class:`str` or :class:`int`
            Color to color the string with. This can be a number from the ANSI 8-bit color codes
            (between 0 and 255) or a string of one of the predefined colors: ``"white"``,
            ``"black"``, ``"light_gray"``, ``"dark_gray"``, ``"gold"``,
            ``"red"``, ``"blue"``, ``"green"``, ``"magenta"``, ``"mint"``,
            ``"orange"``.
    
    Returns
        :class:`str`
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: in-block

        import cachai.utilities as chu

        print(chu.strcol("Magenta text",c="magenta"))

    .. raw:: html

        <div class="out-block highlight-text notranslate">
        <div class="highlight">
            <pre><span style="color:#d700ff;background:#F5FAF7;font-size:12px">Magenta text</span></pre>
        </div>
        </div>
    """
    if isinstance(c,int):
        if (c >= 0) and (c <= 255): return f'\033[38;5;{c}m{string}\033[0m'
        else: return string
    else:
        if c not in _fstr_colors: return string
        return f'\033[38;5;{_fstr_colors[c]}m{string}\033[0m'

def strcol_palette():
    """
    Displays a visual palette of all available ANSI 256-color codes for terminal text coloring.
    
    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: mock-block

        import cachai.utilities as chu

        chu.strcol_palette()
    """
    for i in range(16):
        for j in range(16):
            print(strcol('■',c=i+j*16) + f' {str(i+j*16):<3.3}  ',end='')
        print()