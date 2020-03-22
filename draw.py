"""
Description:
    Functions used to display optical systems and effects
"""

import numpy as np
import matplotlib.pyplot as plt

def draw_system(plt,ax,sys):
    """
    Description:
        Used to draw a system

    plt:    Figure to plot on
    ax:     Plot to draw surface on
    sys:    System to plot
    """

    pos = 0
    for i in sys.elements:
        if i.id == "spherical_lens":
            i.draw(ax,pos)
            pos = pos + i.t
        elif i.id == "thickness":
            pos = pos + i.t 

    max_y = 0.0
    for i in sys.elements:
        if i.id == "spherical_lens":
            if max_y < i.d:
                max_y = i.d
        

    ax.set_xlabel(sys.un) 
    ax.set_ylabel(sys.un) 
    ax.axhline(y=0,color="black",dashes=[5,1,5,1],linewidth=1)
    plt.ylim(-max_y,max_y)
    plt.xlim(0,pos)

def draw_spherical_surface(ax,r,d,p,un):
    """
    Description:
        Used to draw a spherical surface

    ax: Plot to draw surface on
    r:  Radius of curvature
    d:  Diameter
    p:  Position of apex along the optical axis   
    un: Units 
    """

    if r > 0:
        y = np.linspace(-d/2,d/2,1000)
        x = np.sqrt(r**2 + y**2) - r + p
    elif r < 0:
        y = np.linspace(-d/2,d/2,1000)
        x = np.sqrt(r**2 - y**2) + r + p  
    elif r == 0:
        y = np.linspace(-d/2,d/2,1000)  
        x = p + y*0  

    ax.plot(x,y,'b',linewidth=1)

    return(x,y)

def draw_spherical_lens(ax,r1,r2,d,p,t,un):
    """
    Description:
        Used to draw a spherical lens

    ax: Plot to draw lens on
    r1: Radius of curvature of first surface
    r2: Radius of curvature of second surface
    d:  Diameter
    p:  Position of apex along the optical axis 
    t:  Thickness of lens  
    un: Units 
    """

    x1,y1 = draw_spherical_surface(ax,r1,d,p,un)
    x2,y2 = draw_spherical_surface(ax,-r2,d,(p + t),un)

    ax.plot([x1[0],x2[0]],[y1[0],y2[0]],'b',linewidth=1)
    ax.plot([x1[-1],x2[-1]],[y1[-1],y2[-1]],'b',linewidth=1)

def draw_thin_lens(ax,r,d,p,un):
    """
    Description:
        Used to draw a thin lens

    ax: Plot to draw lens on
    r: Radius of curvature
    d:  Diameter
    p:  Position of thin lens center along the optical axis  
    un: Units 
    """
    
    if r > 0: 
        x1,y1 = draw_spherical_surface(ax,r,d,p,un)
        dp = max(x1) - min(x1)
        draw_spherical_surface(ax,-r,d,(p + 2*dp),un)
    elif r < 0:
        x1,y1 = draw_spherical_surface(ax,r,d,p,un)
        dx = max(x1) - min(x1)
        x2,y2 = draw_spherical_surface(ax,-r,d,(p + dx),un)

        ax.plot([x1[0],x2[0]],[y1[0],y2[0]],'b',linewidth=1)
        ax.plot([x1[-1],x2[-1]],[y1[-1],y2[-1]],'b',linewidth=1)

def draw_ray(ax,points,un):
    """
    Description:
        Used to draw a ray

    ax:     Plot to draw lens on
    points: Points of instersection of the ray and system 
    un: Units 
    """

    x = [row[0] for row in points]
    y = [row[1] for row in points]

    ax.plot(x,y,linewidth=2)



if __name__ == "__main__":
    
    fig,ax = plt.subplots()

    draw_spherical_lens(ax,25,25,10,20,2,"mm")
    draw_spherical_lens(ax,-25,-25,10,30,2,"mm")

    plt.show()