"""
Description:
    Functions used to render visuals
"""

import numpy as np
import matplotlib.pyplot as plt

def draw_paraxial_system(ax, sys):
    """
    Draws a paraxial system

    ax:     plot
    sys:    system
    """

    # plot optical axis
    ax.axhline(y=0,color="black",dashes=[5,1,5,1],linewidth=1)

    # plot rays
    y_max = 0
    for ray in sys.rays:
        x = []
        y = []
        for pt in ray.pts:
            x.append(pt[0])
            y.append(pt[1])
            if pt[1] > abs(y_max):
                y_max = abs(pt[1])
        ax.plot(x, y, lw=1)
    y_max = 1.2 * y_max
    plt.ylim(-y_max, y_max)

    # plot starting point
    p = 0
    ax.axvline(p, c="green", ls="--", lw=1)

    # plot lenses
    for i in sys.elements:
        if i.id == "thickness":
            p = p + i.t / i.n
        else:
            r = ((i.d / 2) + y_max) / (2 * y_max)
            ax.axvline(p, color = "blue", ymin = 1 - r, ymax = r, ls = ":" , lw = 1)
            ax.scatter(p, -i.d / 2, color = "blue", marker = 6)
            ax.scatter(p, i.d / 2, color = "blue", marker = 7)
    
    # plot vertex planes
    ax.scatter(sys.v[0], 0, color = "black", marker = ".")
    ax.annotate("V", (sys.v[0], 0))
    ax.scatter(sys.v[1], 0, color = "black", marker = ".")
    ax.annotate("V'", (sys.v[1], 0))

    # plot principal planes
    ax.scatter(sys.pp[0], 0, color = "black", marker = ".")
    ax.annotate("P", (sys.pp[0], 0))
    ax.scatter(sys.pp[1], 0, color = "black", marker = ".")
    ax.annotate("P'", (sys.pp[1], 0))

    # plot focal planes
    ax.scatter(sys.fp[0], 0, color = "black", marker = ".")
    ax.annotate("F", (sys.fp[0], 0))
    ax.scatter(sys.fp[1], 0, color = "black", marker = ".")
    ax.annotate("F'", (sys.fp[1], 0))

    # plot ending point
    ax.axvline(p, c="red", ls="--", lw=1)

    

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