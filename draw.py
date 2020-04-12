"""
Description:
    Functions used to render visuals
"""

import numpy as np
import matplotlib.pyplot as plt

import elements, paraxial

def draw_surface(ax, x, y):
    """
    Description:
        Used to draw a surface

    ax: Plot to draw surface on
    x:  x points
    y:  y points
    """

    ax.plot(x, y, 'b', linewidth = 1)

def draw_lens(ax, coords):
    """
    Description:
        Used to draw a lens (mainly just to connect the surfaces)

    ax:     Plot to draw surface on
    coords: Points from surfaces
    """

    for i in range(len(coords) - 1):
        ax.plot([coords[i][0][0], coords[i + 1][0][0]], [coords[i][0][1], coords[i + 1][0][1]], 'b', linewidth=1)
        ax.plot([coords[i][-1][0], coords[i + 1][-1][0]], [coords[i][-1][1], coords[i + 1][-1][1]], 'b', linewidth=1)