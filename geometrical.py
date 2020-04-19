"""
This module deals with first order optics
"""

import numpy as np

from draw import draw_paraxial_system

### FUNCTIONS ###

###  CLASSES  ###

class Lens():
    """
    Holds a thin spherical lens
    """

    id = "lens"

    def __init__(self, f):
        """
        Defines a thin lens

        f:  focal length of lens
        """

        self.f = f

        # power of lens
        self.phi = 1 / self.f


class Thickness():
    """
    Holds a thickness
    """

    id = "thickness"

    def __init__(self, t, n):
        """
        Defines a thickness

        t:  thickness
        n:  refractive index
        """

        self.t = t
        self.n = n


class System():
    """
    Holds a system
    """

    id = "system"

    def __init__(self):
        """
        Defines a system
        """

        self.elements = []
        self.rays = []
    
    def add_element(self,element):
        """
        Adds an element to the system

        element:    element to be added
        """

        self.elements.append(element)
    
    def add_elements(self,elements):
        """
        Adds list of elements to the system

        elements:   list of elements to be added
        """
        
        for  i in elements:
            self.elements.append(i)
         
    def trace_ray(self, ray):
        """
        Traces a ray through the system

        ray:    ray to be traced
        """
        # postion of elements
        p = 0

        # input ray
        pos = np.array([
            ray.pts[0][1], 
            ray.pts[0][2]
            ])
      
        for i in range(len(self.elements)):

            element = self.elements[i]

            if element.id == "thickness":
                
                # updates postion
                p = p + element.t

                # transfer array
                transfer = np.array([
                    [1, element.t / element.n],
                    [0, 1]
                    ])

                # ouput ray
                pos = np.matmul(transfer, pos) 

                # append point to ray points
                ray.pts = np.append(ray.pts, np.array([[p, pos[0], pos[1]]]), axis=0)
            
            elif element.id == "lens":

                # refraction array
                refraction = np.array([
                    [1, 0],
                    [-element.phi, 1]
                    ])

                # output ray
                pos = np.matmul(refraction, pos)
        
        self.rays.append(ray)
        
        return pos

    def draw(self, ax):
        """
        Draws the system

        ax: plot
        """

        draw_paraxial_system(ax, self)


class Ray():
    """
    Holds a ray
    """

    id = "ray"

    def __init__(self, y, u):
        """
        Defines a ray

        y:  ray height
        u:  paraxial ray angle
        """

        self.y = y
        self.u = u

        """
        Array of points to store all points in a ray

        Format
            [
                [p0, y0, u0],
                ...
                [pn, yn, un]
            ]
        """
        self.pts = np.array([[0, self.y, self.u]])


if __name__ == "__main__":
    """
    Space for testing
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    t0 = Thickness(50, 1)
    lens1 = Lens(500)
    t1 = Thickness(600, 1)
    lens2 = Lens(100)
    t2 = Thickness(100, 1)
    ray1 = Ray(600, 0)
    ray2 = Ray(-600, 0)

    sys = System()
    sys.add_elements([t0, lens1, t1, lens2, t2])
    sys.trace_ray(ray1)
    sys.trace_ray(ray2)

    sys.draw(ax)

    plt.show()
