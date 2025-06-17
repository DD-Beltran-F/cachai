# Imports
import numpy as np
import colorsys
# Matplotlib imports
from matplotlib import pyplot as plt
# Scipy imports
from scipy.spatial.distance import cdist
from scipy.interpolate import interp1d

# f-string pre-defined colors
fstr_colors = {'white':255,'black':232,'light_gray':245,'dark_gray':237,'gold':220,
               'red':196,'blue':21,'green':118,'magenta':165,'mint':87,'orange':202}

# Print the pyhton color palette (256) for strings
def color_palette():
    for i in range(16):
        for j in range(16):
            print(textco('■',c=i+j*16) + f' {str(i+j*16):<3.3}  ',end='')
        print()

# Function to add color to prints
def textco(text,c='white'):
    if is_int(c):
        return f'\033[38;5;{c}m{text}\033[0m'
    else:
        try:
            temp = fstr_colors[c]
        except:
            c = 'white'
        return f'\033[38;5;{fstr_colors[c]}m{text}\033[0m'

# Convert color from rgb to hsl
def rgb_to_hsl(rgb):
    r,g,b = rgb
    h,l,s = colorsys.rgb_to_hls(r,g,b)
    return (h,s,l)

# Convert color from hsl to rgb 
def hsl_to_rgb(hsl):
    h,s,l = hsl
    r,g,b = colorsys.hls_to_rgb(h, l, s)
    return (r,g,b)

# Saturation
def saturate_color(color,factor=1):
    h,s,l = rgb_to_hsl(color)
    s_new = max(0, min(1,s*factor))
    r,g,b = hsl_to_rgb((h,s_new,l))
    return (r,g,b)

# Alpha
def alpha_color(color, alpha=1, bg=(1,1,1)):
    r,g,b = color
    bg_r,bg_g,bg_b = bg
    factor = max(0, min(1, alpha))
    r_result = (r*factor) + (bg_r*(1-factor))
    g_result = (g*factor) + (bg_g*(1-factor))
    b_result = (b*factor) + (bg_b*(1-factor))
    return (r_result,g_result,b_result)

# Lighter color
def lighter_color(color,p=0.1):
    r,g,b = color
    factor = max(0, factor)
    r = min(1, r + (1-r)*factor)
    g = min(1, g + (1-g)*factor)
    b = min(1, b + (1-b)*factor)
    return (r,g,b)

# Darker color
def darker_color(color,factor=0.1):
    r,g,b = color
    factor = 1 - (max(0,factor))
    r = max(0, r*factor)
    g = max(0, g*factor)
    b = max(0, b*factor)
    return (r,g,b)

# Modify color
def mod_color(color,light=1,sat=1,alpha=1,alpha_bg=(1,1,1)):
    new_color = color
    # Light
    if light > 1:
        new_color = lighter_color(new_color,factor=light-1)
    elif light < 1:
        new_color = darker_color(new_color,factor=1-light)
    # Saturation
    new_color = saturate_color(new_color,factor=sat)
    # Alpgha
    new_color = alpha_color(new_color,alpha=alpha,bg=alpha_bg)
    return new_color


def angspace(alpha,beta,n=200):
    """Generate a linear space of angles"""
    theta = abs(beta-alpha)
    ndots = int(theta*n/(2*np.pi))
    return np.linspace(alpha,beta,ndots)
    
def angdist(alpha,beta):
    """Compute the minimum angular distance"""
    diff = np.abs(alpha - beta) % (2 * np.pi)
    return np.min([diff, 2 * np.pi - diff])

def quadratic_bezier(t,P0:list,P1:list,P2:list):
    """Evaluate quadratic bezier curve in t"""
    if (P0 is None) or (P1 is None) or (P2 is None): return None
    P0 = np.array(P0); P1 = np.array(P1); P2 = np.array(P2)
    return (1-t)**2 * P0 + 2*(1-t)*t * P1 + t**2 * P2

def get_bezier_curve(P0:list,P1:list,P2:list,n=20):
    """Create quadratic bezier curve points [x,y]"""
    if (P0 is None) or (P1 is None) or (P2 is None): return None
    t_values = np.linspace(0, 1, n)
    return np.array([quadratic_bezier(t, P0, P1, P2) for t in t_values])

def equidistant(points):
    """Make any array of points equidistant"""
    # Cumulative distances between consecutive points
    diffs = np.diff(points, axis=0)
    distances = np.linalg.norm(diffs, axis=1)
    cumulative_length = np.insert(np.cumsum(distances), 0, 0)

    # Interpolation
    total_length = cumulative_length[-1]
    new_distances = np.linspace(0, total_length, len(points))

    interp_x = interp1d(cumulative_length, points[:, 0], kind='linear')
    interp_y = interp1d(cumulative_length, points[:, 1], kind='linear')
    
    # Equidistant curve
    new_x = interp_x(new_distances)
    new_y = interp_y(new_distances)
    
    return np.column_stack((new_x, new_y))

def map_from_curve(curve=None,xlims=(-1,1),ylims=(-1,1),resolution=200):
    """Map points using the distance to curve"""
    if curve is None: return None
    
    # Colors values from curve
    colors = np.linspace(-1,1,len(curve))
    
    # Mesh
    x = np.linspace(*xlims, resolution)
    y = np.linspace(*ylims, resolution)
    grid_x, grid_y = np.meshgrid(x, y, indexing='xy')
    grid_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))

    # Obtain the nearest point in the curve and use that color
    distances             = cdist(grid_points, curve)
    nearest_point_indexes = np.argmin(distances, axis=1)
    map_flat              = colors[nearest_point_indexes]
    map_matrix            = map_flat.reshape(resolution, resolution)
    
    return map_matrix

def colormapped_patch(patch,map_matrix,ax=None,colormap='coolwarm',
                      zorder=5,alpha=0.5,rasterized=False):
    """Plot a color coded patch using a map matrix from map_from_curve"""
    if ax is None: ax = plt.gca()
    
    vertices = patch.get_path().vertices
    xmin, ymin = np.min(vertices, axis=0)
    xmax, ymax = np.max(vertices, axis=0)
    
    img = ax.imshow(map_matrix, 
                    cmap=colormap, 
                    extent=(xmin, xmax, ymin, ymax), 
                    origin='lower',
                    aspect='auto',
                    clip_path=patch,
                    clip_on=True,
                    zorder=zorder,
                    alpha=alpha,
                    rasterized=rasterized,
                    vmin=-1, vmax=1)
    return img