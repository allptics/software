"""
Decription:
    This module is for modeling focal and afocal systems using geometrical optics
"""

import numpy as np
from draw import draw_paraxial_system

### ELEMENTS ###
class Element():
    """
    Parent class for elements
        
        ID Reference
            Unassigned: None
            Object:     object
            Image:      image
            ThinLens:   thin-lens
            Aperture:   aperture
            Thickness:  thickness
            Rays:       ray

            System:     system
    """
    physics_sys = "geometrical"
    id = None

class Object(Element):
    """
    Child class for objects
    """
    id = "object"

    def __init__(self, h = None, offset = 0):
        """
        Defines an object

        h:      axial height of object
        offset: axial offset (default object starts on axis)
        """
        self.h = h

class Image(Element):
    """
    Child class for images
    """
    id = "image"

    def __init__(self, h = None, offset = 0):
        """
        Defines an image

        h:      axial height of image
        offset: axial offset (default image starts on axis)
        """
        self.h = h

class ThinLens(Element):
    """
    Child class for thin lenses (spherical)
    """
    id = "thin-lens"

    def __init__(self, f, d):
        """
        Defines a thin lens (spherical)

        f:  focal length of lens
        d:  diameter of lens
        """7
        self.f = f
        self.d = d

        # power of lens
        self.phi = 1 / self.f
        
        ## CONDITIONALS ##
        self.isSystemStop = False

class Aperture(Element):
    """
    Child class for apertures
    """
    id = "aperture"

    def __init__(self, d):
        """
        Defines an aperture

        d:  diameter of aperture
        """
        self.d = d

        ## CONDITIONALS ##
        self.isSystemStop = False

class Thickness(Element):
    """
    Child class for thicknesses
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

        # reduced thickness
        self.T = t / n

###   RAYS   ###
class Ray(Element):
    """
    Class for a ray
    """
    id = "ray"

    def __init__(self, y, u, p = 0):
        """
        Defines a ray

        y:      ray height
        u:      paraxial ray angle
        p:      starting position of ray
        """
        self.y = y
        self.u = u
        self.p = p

        """
        Array of ray points
            [
                [p0, y0, u0],
                ...
                [pn, yn, un]
            ]
        """
        self.pts = np.array([[self.p, self.y, self.u]])

###  SYSTEM  ###
class System(Element):
    """
    Class for a system
    """
    id = "system"

    def __init__(self, type="focal"):
        """
        Defines a system
        """

        self.type = "focal"
        self.elements = []
        self.rays = []

        # current reduced thickness
        self.p = 0

        # principal planes
        self.pp = [None, None]
        # focal planes
        self.fp = [None, None]
        # vertexs
        self.v = [None, None]

        # system stop id and position
        self.stop = [None, None]
    
    # Functions for adding elements/rays/planes to system

    def add_element(self,element):
        """
        Adds an element to the system

        element:    element to be added
        """

        p = self.p

        if element.id == "thickness":
            self.p = self.p + element.t / element.n
        else:
            pass

        self.elements.append([p, element])
    
    def add_elements(self,elements):
        """
        Adds list of elements to the system

        elements:   list of elements to be added
        """
        
        for i in elements:
            self.add_element(i)
    
    def transfer(self, pos, element):
        """
        Performs a transfer

        pos:        intial ray array
        element:    either a thickness or thin lens 
        """
        # reduced thickness
        t = element.t / element.n
        # transfer array
        transfer = np.array([
            [1, t],
            [0, 1]
        ])
        # ouput ray
        pos = np.matmul(transfer, pos)

        return pos

    def refraction(self, pos, element):
        """
        Performs a refraction

        pos:        intial ray array
        element:    either a thickness or thin lens
        """
        # refraction
        refraction = np.array([
            [1, 0],
            [-element.phi, 1]
        ])
        # output ray
        pos = np.matmul(refraction, pos)

        return pos

    def trace_ray(self, ray):
        """
        Traces ray through the system

        ray:    ray to be traced
        """
        # postion of elements
        p = 0
        # initial ray height
        y = ray.pts[0][1]
        # initial ray angle
        u = ray.pts[0][2]
        # initial ray array
        pos = np.array([y, u])
      
        for i in range(len(self.elements)):
            try:
                p = self.elements[i + 1][0]
            except:
                pass
            element = self.elements[i][1]

            if element.id == "thickness":
                # transfer
                pos = self.transfer(pos, element)
                # point array
                pt = np.array([[p, pos[0], pos[1]]])
                # append point to ray points
                ray.pts = np.append(ray.pts, pt, axis=0)
            
            elif element.id == "lens":
                # refraction
                pos = self.refraction(pos, element)

    def add_ray(self, ray):
        """
        Adds a ray to the system

        ray:    ray to be added
        """
        
        self.trace_ray(ray)
        
        self.rays.append(ray)

    def add_planes(self):
        """
        Adds planes to the system
        """
        self.find_vertex_points()
        self.pp = [self.v[0] + self.find_front_principal_plane(), self.v[1] + self.find_rear_principal_plane()]
        self.fp = [self.v[0] + self.find_front_focal_distance(), self.v[1] + self.find_back_focal_distance()]

    def find_system_stop(self):
        """
        Finds the system stop
        """
        stopID = None
        stopPos = None
        minRatio = None
        isFirst = True

        # ray starting at axial object postion with arbitrary angle
        ray = Ray(0, 0.001)
        self.trace_ray(ray)

        # removes the intial and exiting thicknesses
        elements = self.elements[1:-1]

        j = 1
        for i in range(len(elements)):
            p = self.elements[i][0]
            element = self.elements[i][1]
            
            if element.id == "lens" or element.id == "stop":
                pt = ray.pts[j]
                ratio = (element.d / 2) / pt[1]
                if isFirst:
                    stopID = i
                    stopPos = p
                    minRatio = ratio
                    isFirst = False
                else:
                    stopID = i
                    stopPos = p
                    minRatio = ratio

        self.elements[stopID][1].isSystemStop = True
        self.stop = [stopID, stopPos]

    # Functions for making system calculations

    def find_vertex_points(self):
        """
        Finds the vertex points
        """
        isFirst = True

        for i in range(len(self.elements)):
            p = self.elements[i][0]
            element = self.elements[i][1]

            if element.id == "lens":
                if isFirst:
                    self.v[0] = p
                    isFirst = False
                self.v[1] = p

    def find_vertex_matrix(self):
        """
        Returns the vertex matrix
        """
        # removes the intial and exiting thicknesses
        elements = self.elements[2:-2]
        elements = [row[1] for row in elements]
        # intializes vertex matrix
        vertex_matrix = np.array([
            [1, 0],
            [-elements[0].phi, 1]
        ])

        # sets up max
        max = len(elements)
        # sets up increment
        i = 1

        while i < max:
            element = elements[i]
            i = i + 1  
            if element.id == "thickness":
                # transfer array
                transfer = np.array([
                    [1, element.t / element.n],
                    [0, 1]
                ])   
                # update vertex matrix 
                vertex_matrix = np.matmul(transfer, vertex_matrix)

            elif element.id == "lens":
                refraction = np.array([
                    [1, 0],
                    [-element.phi, 1]
                ])
                # update vertex matrix 
                vertex_matrix = np.matmul(refraction, vertex_matrix)
        
        return vertex_matrix

    def find_power(self):
        """
        Returns the system power
        """
        # find the system matrix
        vertex_matrix = self.find_vertex_matrix()
        # find power
        phi = -vertex_matrix[1][0]

        return phi
    
    def find_effective_focal_length(self):
        """
        Returns the effective focal length
        """
        # finds effective focal length
        f = 1 / self.find_power()

        return f

    def find_front_focal_length(self):
        """
        Returns the front focal length (relative to front principal plane)
        """
        # finds the front focal length
        f_f = - 1 / self.find_power()

        return f_f

    def find_rear_focal_length(self):
        """
        Returns the rear focal length (relative to rear principal plane)
        """
        # finds the rear focal length
        f_r = 1 / self.find_power()

        return f_r
    
    def find_front_principal_plane(self):
        """
        Returns the front principal plane (relative to first vertex)
        """
        # find the vertex matrix
        vertex_matrix = self.find_vertex_matrix()
        # finds the front principal plane
        p_f = (vertex_matrix[1][1] - 1) / vertex_matrix[1][0]
    
        return p_f
    
    def find_rear_principal_plane(self):
        """
        Returns the rear principal plane (relative to last vertex)
        """
        # find the vertex matrix
        vertex_matrix = self.find_vertex_matrix()
        # finds the front principal plane
        p_r = (1 - vertex_matrix[0][0]) / vertex_matrix[1][0]

        return p_r

    def find_front_focal_distance(self):
        """
        Returns the front focal distance (relative to first vertex)
        """
        # find the vertex matrix
        vertex_matrix = self.find_vertex_matrix()
        # finds the front focal distance
        FFD = vertex_matrix[1][1] / vertex_matrix[1][0]

        return FFD
    
    def find_back_focal_distance(self):
        """
        Returns the back focal distance (relative to last vertex)
        """
        # find the vertex matrix
        vertex_matrix = self.find_vertex_matrix()
        # finds the front focal distance
        BFD = - vertex_matrix[0][0] / vertex_matrix[1][0]

        return BFD

    # Functions for displaying system

    def draw(self, ax):
        """
        Draws the system

        ax: plot
        """

        draw_paraxial_system(ax, self)


if __name__ == "__main__":
    """
    Space for testing
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    obj = Object(10)
    t0 = Thickness(50, 1)
    lens1 = ThinLens(100, 20)
    t1 = Thickness(50, 1)
    lens2 = ThinLens(75, 20)
    t2 = Thickness(100, 1)
    img = Image()
    ray1 = Ray(10, 0)

    sys = System()
    sys.add_elements([obj, t0, lens1, t1, lens2, t2, img])
    sys.add_ray(ray1)

    sys.add_planes()
    sys.find_system_stop()

    sys.draw(ax)
    plt.show()