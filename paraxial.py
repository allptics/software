"""
Description:
    Functions used to create paraxial systems
"""

import matplotlib.pyplot as plt
import numpy as np
import draw

class System:
    
    physics_system = "paraxial"

    def __init__(self,un):
        """
        Description:
            Define a spherical lens

        n: Global index of the system
        """

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

        element:    elements to be added
        """
        
        for  i in elements:
            self.elements.append(i)

    def send_ray(self,ray):
        """
        Description:
            Sends ray through a surface
        
        ray:    Ray to send through the surface
        """

        ray.points = ray.points[:1]

        pos = 0
        for i in self.elements:
            pos = pos + i.t
            ray.points.append([pos,ray.points[-1][1],ray.points[-1][2]])

        print(ray.points)


    def draw(self,plt,ax):

        draw.draw_system(plt,ax,self)       

class Lens:

    id = "spherical_lens"
    physics_system = "paraxial"

    def __init__(self,r1,r2,d,t,n,un):
        """
        Description:
            Define a spherical lens

        r1: Radius of curvature of first surface
        r2: Radius of curvature of second surface
        d:  Diameter
        t:  Thickness of lens
        n:  Index of lens  
        un: Units 
        """

        self.surfaces = [Surface(r1,d,un),Surface(r2,d,un)]
        self.d = d
        self.t = t
        self.index = n
        self.un = un

    def draw(self,ax,p):

        draw.draw_spherical_lens(ax,self.surfaces[0].r,self.surfaces[1].r,self.d,p,self.t,self.un)

class Surface:

    id = "spherical_lens"
    physics_system = "paraxial"
    t = 0

    def __init__(self,r,d,un):
        """
        Description:
            Defines a spherical surface

        r:  Radius of curvature
        d:  Diameter
        p:  Position of apex along the optical axis   
        un: Units 
        """

        self.r = r
        self.d = d
        self.un = un

    def draw(self,ax,p):

        draw.draw_spherical_surface(ax,self.r,self.d,p,self.un)

class Thickness:

    id = "thickness"
    physics_system = "paraxial"

    def __init__(self,t,n,un):
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

class Ray:
    
    physics_system = "paraxial"

    def __init__(self,y,u,un):
        """
        Description:
            Define a thickness

        y:  Height of ray from optical axis
        n:  Angle of ray relative to optical axis
        un: Units
        """

        self.points = [[0,y,u]]
        self.un = un
    
    def draw(self,ax):

        draw.draw_ray(ax,self.points,self.un)

if __name__ == "__main__":

    fig,ax = plt.subplots()

    t1 = Thickness(5,1,"mm")
    surf = Surface(100,10,"mm")
    t2 = Thickness(5,1,"mm")
    sys = System("mm")
    sys.add_elements([t1,surf,t2])

    ray = Ray(4,0,"mm")
    sys.send_ray(ray)

    sys.draw(plt,ax)
    ray.draw(ax)

    """
    t1 = Thickness(20,1,"mm")
    lens1 = Lens(100,100,10,1,1,"mm")
    t2 = Thickness(20,1,"mm")
    lens2 = Lens(100,100,20,2,1,"mm")
    t3 = Thickness(20,1,"mm")
    lens3 = Lens(100,100,10,1,1,"mm")

    sys = System("mm")
    sys.add_elements([t1,lens1,t2,lens2,t3,lens3])
    sys.draw(plt,ax)
    """

    plt.show()