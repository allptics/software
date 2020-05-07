"""
Decription:
    This module is for modeling focal and afocal systems using geometrical optics
"""

import numpy as np
from draw import draw_paraxial_system

class Environment():
    """
    Parent class for elements, used to keep physics systems isolated
    """
    physics_sys = "geometrical"

class Object(Environment):
    """
    Child class for objects
    """
    def __init__(self, h = None, offset = 0):
        """
        Defines an object

        h:      axial height of object
        offset: axial offset (default: object starts on axis)
        """
        self.h = h
        self.offset = offset

class Image(Environment):
    """
    Child class for images
    """
    def __init__(self, h = None, offset = 0):
        """
        Defines an image

        h:      axial height of image
        offset: axial offset (default image starts on axis)
        """
        self.h = h
        self.offset = offset

class ThinLens(Environment):
    """
    Child class for thin lenses (spherical)
    """
    def __init__(self, f, d, offset = 0):
        """
        Defines a thin lens (spherical)

        f:  focal length of lens
        d:  diameter of lens
        offset: axial offset (default image starts on axis)
        """
        self.f = f
        self.d = d
        self.offset = offset

        # power of lens
        self.phi = 1 / self.f
        
        ## CONDITIONALS ##
        self.isSystemStop = False

class Aperture(Environment):
    """
    Child class for apertures
    """
    def __init__(self, d):
        """
        Defines an aperture

        d:  diameter of aperture
        offset: axial offset (default image starts on axis)
        """
        self.d = d
        self.offset = offset

        ## CONDITIONALS ##
        self.isSystemStop = False

class Thickness(Environment):
    """
    Child class for thicknesses
    """
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

class Ray(Environment):
    """
    Class for a ray
    """
    def __init__(self, y, u, p = 0):
        """
        Defines a ray

        y:  initial ray height
        u:  initial paraxial ray angle
        p:  initial position of ray on optical axis

        Ray points
            [
                [p0, y0, u0],
                ...
                [pn, yn, un]
            ]
        """
        self.pts = np.array([
            [p, y, u]
        ])

class System(Environment):
    """
    Class for a system
    """
    def __init__(self, sys_type = "focal"):
        """
        Defines a system
        """
        self.sys_type = sys_type
        
        self.list = {
            "obj": None,
            "img": None,
            "elements": [],
            "rx": [],
            "pp": [None, None],
            "ff": [None, None],
            "vv": [None, None],
            "rays": []
        }
    
    # Functions for adding elements/rays/planes to system

    def update_perscription(self):
        """
        Updates the system perscription
        """
        # clears previous perscription
        self.list["rx"].clear()
        # intial reduced postion
        p = 0

        for element in self.list["elements"]:
            id = type(element).__name__

            self.list["rx"].append({"p": p, "id": id})

            if id == "Thickness":
                p = p + element.T

    def add_element(self,element):
        """
        Adds an element to the system

        element:    element to be added
        """
        id = type(element).__name__

        if id == "Object":
            self.list["obj"].append(element)
            self.list["img"] = None
        elif id == "Image":
            self.list["obj"] = None
            self.list["img"].append(element)
        else:
            self.list["elements"].append(element)
        
        self.update_perscription()
        
    def add_elements(self,elements):
        """
        Adds list of elements to the system

        elements:   list of elements to be added
        """
        for i in elements:
            self.add_element(i)
    
    def transfer(self, inital, element):
        """
        Performs a transfer

        initial:        intial ray array
        element:    either a thickness or thin lens 
        """
        # transfer array
        transfer = np.array([
            [1, element.T],
            [0, 1]
        ])
        # ouput ray
        output = np.matmul(transfer, inital)

        return output

    def refraction(self, initial, element):
        """
        Performs a refraction

        initial:        intial ray array
        element:    either a thickness or thin lens
        """
        # refraction
        refraction = np.array([
            [1, 0],
            [-element.phi, 1]
        ])
        # output ray
        output = np.matmul(refraction, initial)

        return output

    def trace_ray(self, ray, dir = 1):
        """
        Traces ray through the system

        ray:    ray to be traced
        dir:    direction to trace (1 forward, -1 backwards)
        """
        # intial ray array
        initial = np.array([ray.pts[0][1], ray.pts[0][2]])
        # starting position of array
        p = ray.pts[0][0]
      
        for element in self.list["elements"]:

            id = type(element).__name__

            if id == "Thickness":
                # transfer
                output = self.transfer(initial, element)
                # increment thickness
                p = p + element.T
                # point array
                pt = np.array([[p, output[0], output[1]]])
                # append point to ray points
                ray.pts = np.append(ray.pts, pt, axis=0)
            
            elif id == "ThinLens":
                # refraction
                output = self.refraction(initial, element) 

            initial = output       

    def add_ray(self, ray):
        """
        Adds a ray to the system

        ray:    ray to be added
        """
        self.trace_ray(ray)
        self.list["rays"].append(ray)

    def find_planes(self):
        """
        Finds the planes to the system
        """
        # finds the vertices
        self.list["vv"][0] = self.list["rx"][1]
        self.list["vv"][1] = self.list["rx"][-2]

        # finds the principal planes
        self.list["pp"][0] = self.list["vv"][0] + self.find_front_principal_plane()
        self.list["pp"][1] = self.list["vv"][1] + self.find_rear_principal_plane()
        
        # finds the focal planes
        self.list["ff"][0] = self.list["vv"][0] + self.find_front_focal_distance()
        self.list["ff"][1] = self.list["vv"][1] + self.find_back_focal_distance()

    # Functions for making system calculations

    def find_vertex_matrix(self):
        """
        Updates the vertex matrix
        """
        # removes the intial and exiting thicknesses
        elements = self.list["elements"]

        # remove bounding thicknesses
        while type(elements[0]).__name__ == "Thickness":
            del elements[0]
        while type(elements[len(elements) - 1]).__name__ == "Thickness":
            del elements[len(elements) - 1]

        # reverse for multiplication
        elements.reverse()

        print(elements[0].f)
        exit()

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
            if element.id == "Thickness":
                # transfer array
                transfer = np.array([
                    [1, element.t / element.n],
                    [0, 1]
                ])   
                # update vertex matrix 
                vertex_matrix = np.matmul(transfer, vertex_matrix)

            elif element.id == "ThinLens":
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

    t0 = Thickness(100, 1)
    lens0 = ThinLens(100, 10)
    t1 = Thickness(100, 1)
    lens1 = ThinLens(-100, 10)
    t2 = Thickness(100, 10)

    ray0 = Ray(10, 0)
    ray1 = Ray(5, 0)
    ray2 = Ray(2.5, 0)

    sys = System()
    sys.add_elements([t0, lens0, t1, lens1, t2])
    sys.add_ray(ray0)
    sys.find_vertex_matrix()    