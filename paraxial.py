"""
Description:
    Functions used to create paraxial systems
"""

import numpy as np

import draw

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

    def __init__(self, phi = None, d = None, p = 0):
        """
        Defines a thin lens
        
        phi:    power of lens
        d:      diameter of lens 
        p:      position of lens on optical axis
        """

        self.phi = phi
        self.d = d

        self.V0 = self.V1 = self.P0 = self.P1 = self.N0 = self.N1 = p
        
        if not phi == None:
            self.f = 1 / self.phi
        else:
            self.f = None

class Thickness:
    """
    Holds a thickness
    """

    def __init__(self, t, n):
        """
        Initializes a thickness

        t:  Thickness
        n:  Index of refraction
        """

        self.t = t
        self.n = n
        self.T = t*n


class ThickLens:
    """
    Holds a thick lens
    """


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
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()