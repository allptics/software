"""
Description:
    Functions and classes to define elements (i.e. surfaces, thicknesses)
"""

import matplotlib.pyplot as plt
import numpy as np

import draw

class Surface:
    """
    Base class for defining surfaces
    """

    id = "surface"
    type = "undefined"

    # ADD APERTURE
    def __init__(self, d, un):
        """
        Description:
            Defines a surface

        d:  Diameter
        un: Units 
        """

        self.d = d
        self.un = un


class SphericalSurface(Surface):
    """
    Holds spherical surfaces
    """

    type = "spherical"

    def __init__(self, r, d, un):
        """
        Description:
            Defines a spherical surface

        r: Radius of curvature
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

        if self.r > 0:
            y = np.linspace(-self.d/2, self.d/2, 1000)
            x = np.sqrt(self.r**2 + y**2) - self.r + p
        elif self.r < 0:
            y = np.linspace(-self.d/2, self.d/2, 1000)
            x = np.sqrt(self.r**2 - y**2) + self.r + p  
        elif self.r == 0:
            y = np.linspace(-self.d/2, self.d/2, 1000)  
            x = p + y*0  
        
        draw.draw_surface(ax, x, y)

        return np.stack((x, y), axis = -1)


class Thickness:
    """
    Base class for thickness
    """

    id = "thickness"

    def __init__(self, t, n, un):
        """
        Description:
            Define a thickness

        t:  Thickness
        n:  Index of thickness
        un: Units
        """

        self.t = t
        self.n = n
        self.un = un


class Lens:
    """
    Base class for a lens
    """

    id = "lens"
    type = "undefined"

    def __init__(self, un, d = 0, t = 0):
        """
        Description:
            Defines a lens

        elements:   List of surfaces and thicknesses
        d:          Diameter of lens
        t:          Thickness of lens
        un:         Units 
        """

        self.elements = []
        self.d = d
        self.t = t
        self.un = un
    
    def add_element(self,element):
        """
        Description:
            Adds an element to the lens

        element:    Element to be added
        """

        self.elements.append(element)

        try:
            if element.d > self.d:
                self.d = element.d
        except:
            self.d = self.d
        
        if element.id == "thickness":
            self.t = self.t + element.t
    
    def add_elements(self,elements):
        """
        Description:
            Adds list of elements to the system

        elements:    Elements to be added
        """
        
        for i in elements:
            self.add_element(i)
    
    def draw(self, ax, p = 0):
        """
        Description:
            Draws lens
        
        ax: Plot to draw to
        p:  Postion to start  
        """
        
        # array to fill with edge coords
        edges = []
        
        for i in self.elements:
            if i.id == "thickness":
                p = p + i.t               
            else:
                coords = i.draw(ax, p)
                edges.append([coords[0], coords[-1]])
                try:
                    p = p + i.t
                except:
                    p = p

        draw.draw_lens(ax, edges)


if __name__ == "__main__":
    """
    Space for testing
    """
    fig, ax = plt.subplots()

    lens = Lens("mm")
    lens.add_elements([
                        SphericalSurface(150, 10, "mm"), 
                        Thickness(1, 1.5, "mm"),
                        SphericalSurface(150, 10, "mm")
                        ])
    lens.draw(ax, 10)

    plt.show()