"""
Description:
    Functions used to create paraxial systems
"""

import matplotlib.pyplot as plt
import numpy as np

import draw, elements

class System:
    """
    Holds a paraxial optical system
    """
    sys = "paraxial"

    def __init__(self, n, un):
        """
        Description:
            Defines an optical system

        n: Global index of the system
        """

        self.n = n
        self.elements = []
        self.rays = []
        self.un = un

    def add_element(self,element):
        """
        Description:
            Adds an element to the system

        element:    element to be added
        """

        self.elements.append(element)
    
    def add_elements(self,elements):
        """
        Description:
            Adds list of elements to the system

        element:    Elements to be added
        """
        
        for  i in elements:
            self.elements.append(i)
        
    def draw(self, ax, p = 0):
        """
        Description:
            Draws system

        ax: Plot to plot system
        p:  Starting position of system
        """

        max_y = 0
        for i in self.elements:
            if i.id == "thickness":
                p = p + i.t
            else:
                i.draw(ax, p)
                try:
                    p = p + i.t
                except:
                    p = p
                if max_y < i.d:
                        max_y = i.d
        
        ax.set_xlabel(self.un) 
        ax.set_ylabel(self.un) 
        ax.axhline(y=0,color="black",dashes=[5,1,5,1],linewidth=1)
        plt.ylim(-max_y,max_y)
        plt.xlim(0 - p/10 , p + p/10)


class ThinLens:
    """
    Holds a thin lens
    """

    id = "thin"

    def __init__(self, r, d, un):
        """
        Description:
            Defines a thin lens
        
        r:  Radius of curvature
        d:  Diameter
        un: Units
        """

        self.r = r
        self.d = d
        self.un = un
    
    def draw(self, ax, p = 0):
        """
        Description:
            Draws a spherical surface

        ax: Plot to draw surface on
        p: Position of apex along the optical axis 
        """

        draw.draw_thinlens(ax, self.d, p)


class Ray:
    """
    Base class for a paraxial ray
    """

    sys = "paraxial"

    def __init__(self, y, w, un):
        """
        Description:
            Initializes a ray
        
        y:  Height of ray (relative to the optical axis)
        w:  Angle of ray
        un: Units of ray
        """

        self.y = y
        self.w = w
        self.un = un


if __name__ == "__main__":
    """
    Space for testing
    """

    fig, ax = plt.subplots()

    t1 = elements.Thickness(10, 1, "mm")
    thin1 = ThinLens(100, 10, "mm")
    t2 = elements.Thickness(10, 1.5, "mm")
    thin2 = ThinLens(-100, 10, "mm")
    t3 = elements.Thickness(10, 1, "mm")


    sys = System(1, "mm")
    sys.add_elements([
        t1,
        thin1,
        t2,
        thin2,
        t3
    ])

    sys.draw(ax)
    plt.show()