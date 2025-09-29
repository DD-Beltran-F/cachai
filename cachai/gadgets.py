# Basic imports
import numpy as np
# Matplotlib imports
from   matplotlib.text import Text

class PolarText(Text):
    """
    Initialize a :class:`matplotlib.text.Text` instance using polar coordinates.

    Attributes
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

    Other Attributes
        ``**kwargs``
            Keyword arguments of :class:`matplotlib.text.Text`.

    Examples
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: python
        :class: mock-block

        import matplotlib.pyplot as plt
        import cachai.gadgets as chg

        fig, ax = plt.subplots()
        ax.plot([0,0],[1,1])
        polar = chg.PolarText((0,0),1,45,text='Im polar!',pad=0.5,ha='center', va='center')
        ax.add_artist(polar)
        plt.show()
    
    Methods
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    """
    def __init__(self, radius, angle, text, center=(0,0), pad=0.0, **kwargs):
        """:meta private:"""
        self._radius = radius
        self._angle  = np.deg2rad(angle)
        self.center  = np.array(center)
        self._pad    = pad
        
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        
        super().__init__(x, y, text, **kwargs)

    def _polar_to_cartesian(self, radius, angle):
        """:meta private:
        Tranform polar (radius, angle) to catesian (x, y).
        
            radius : :class:`float`
                Radius coordinate.
            angle : :class:`float`
                Angle coordinate in radians.
        """
        dx = radius * np.cos(angle)
        dy = radius * np.sin(angle)
        return self.center + np.array([dx, dy])

    def set_polar_position(self, radius=None, angle=None, center=None):
        """
        Updates multiple polar coordinates simultaneously.

        Parameters
            radius : :class:`float`
                New radial distance from center.
            angle : :class:`float`
                New angular position in degrees.
            center : :class:`tuple` or :class:`array-like`
                New center coordinates for the polar system.
        """
        if radius is not None:
            self._radius = radius
        if angle is not None:
            self._angle = np.deg2rad(angle)
        if center is not None:
            self.center = np.array(center)
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))
    
    def set_pad(self, pad):
        """
        Adjusts the radial padding distance between the text and its base polar position.
        
        Parameters
            pad : :class:`float`
                New padding value.
        """
        self._pad = pad
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))
    
    def set_radius(self, radius):
        """
        Updates the radial coordinate of the text relative to the center point.
        
        Parameters
            radius : :class:`float`
                New radius coordinate.
        """
        self._radius = radius
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))

    def set_angle(self, angle):
        """
        Changes the angular position of the text around the center.
        
        Parameters
            angle : :class:`float`
                New angle coordinate in degrees.
        """
        self._angle = np.deg2rad(angle)
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))

    def set_center(self, center):
        """
        Moves the entire polar coordinate system to a new center point.

        Parameters
            center : :class:`tuple` or :class:`array-like`
                New center coordinates (x,y).
        """
        self.center = np.array(center)
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))