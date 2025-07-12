# Basic imports
import numpy as np
# Matplotlib imports
from   matplotlib.text import Text

class PolarText(Text):
    def __init__(self, center, radius, angle, text='', pad=0.0, **kwargs):
        """
        Initialize a Text instance using polar coordinates.
        
        Parameters:
        -----------
        center : tuple
            Center of the polar system
        radius : float
            Radius coordinate
        theta : float
            Angle coordinate in rad
        text : str
            Text to diplay (default: '')
        pad : float
            Label position adjustment (default: 0.0)
        
        Keyword Arguments:
        -----------------
        From the parent class Text
        """
        self.center  = np.array(center)
        self._radius = radius
        self._angle  = angle
        self._pad    = pad
        
        x, y = self._polar_to_cartesian(radius*(1 + pad), angle)
        
        super().__init__(x, y, text, **kwargs)

    def _polar_to_cartesian(self, radius, angle):
        """Tranform polar (radius, angle) to catesian (x, y)."""
        dx = radius * np.cos(angle)
        dy = radius * np.sin(angle)
        return self.center + np.array([dx, dy])
    
    def set_pad(self, pad):
        """Update pad"""
        self._pad = pad
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))
    
    def set_radius(self, radius):
        """Update radius"""
        self._radius = radius
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))

    def set_angle(self, angle_deg):
        """Update angle in deg"""
        self._angle = np.deg2rad(angle_deg)
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))

    def set_polar_position(self, radius=None, angle_deg=None):
        """Update radius and/or angle"""
        if radius is not None:
            self._radius = radius
        if angle_deg is not None:
            self._angle = np.deg2rad(angle_deg)
        x, y = self._polar_to_cartesian(self._radius*(1 + self._pad), self._angle)
        self.set_position((x, y))