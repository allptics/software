"""
Use to hold equations
"""
import sympy as sym

### CONSTANTS ###

# Speed of light in a vacuum [m/s]
c = 2.99792458 * 10**8

### EQUATIONS ###

class index_of_refraction():
    """
    n = c / v 
    
    n:  index of refraction\n
    c:  speed of light in a vacuum\n
    v:  phase velocity (speed of light in medium)
    """

    def __init__(self):
        """
        Initializes equation
        """
        self.n, self.c, self.v = sym.symbols("n c v")
        self.equation = sym.Eq(self.n, self.c / self.v)
    
    def show(self):
        """
        Shows equation
        """
        sym.pprint(self.equation)
    
    def solve_n(self, v):
        """
        Solves equation for index of refraction

        v:  phase velocity (speed of light in medium)
        """
        equation = self.equation.subs([(self.c, c), (self.v, v)])
        return sym.solve(equation, self.n)[0]

    def solve_m(self, n):
        """
        Solves equation for phase velocity (speed of light in medium)

        n:  index of refraction
        """
        equation = self.equation.subs([(self.c, c), (self.n, n)])
        return sym.solve(equation, self.v)[0]


class wavelength():
    """
    w = v / f

    w:  wavelength\n
    v:  phase velocity (speed of light in medium)\n
    f:  frequency
    """

    def __init__(self):
        """
        Initializes equation
        """
        self.w, self.v, self.f = sym.symbols("w v f")
        self.equation = sym.Eq(self.w, self.v / self.f)
    
    def show(self):
        """
        Shows equation
        """
        sym.pprint(self.equation)

    def solve_w(self, v, f):
        """
        Solves equation for wavelength

        v:  phase velocity (speed of light in medium)
        f:  frequency
        """
        equation = self.equation.subs([(self.v, v), (self.f, f)])
        return sym.solve(equation, self.w)[0]
    
    def solve_v(self, w, f):
        """
        Solves equation for phase velocity (speed of light in medium)

        w:  wavelength
        f:  frequency
        """
        equation = self.equation.subs([(self.w, w), (self.f, f)])
        return sym.solve(equation, self.v)[0]

    def solve_f(self, w, v):
        """
        Solves equation for frequency

        w:  wavelength
        v:  phase velocity (speed of light in medium)
        """
        equation = self.equation.subs([(self.w, w), (self.v, v)])
        return sym.solve(equation, self.f)[0]


class wavenumber():
    """
    wn = 1 / w

    wn: number of wavelengths per cm\n
    w:  wavelength
    """

    def __init__(self):
        """
        Initializes equation
        """
        self.wn, self.w = sym.symbols("wn w")
        self.equation = sym.Eq(self.wn, 1 / self.w)
    
    def show(self):
        """
        Shows equation
        """
        sym.pprint(self.equation)

    def solve_wn(self, w):
        """
        Solves equation for wavenumber

        w:  wavelength
        """
        equation = self.equation.subs(self.w, w)
        return sym.solve(equation, self.wn)[0]

    def solve_w(self, wn):
        """
        Solves equation for wavenumber

        wn: wavenumber
        """
        equation = self.equation.subs(self.wn, wn)
        return sym.solve(equation, self.w)[0]


class snells_law():
    """
    n1 * sin(theta1) = n2 * sin(theta2)

    n1:     incident index of refraction\n
    theta1: incident angle\n
    n2:     exiting index of refraction\n
    theta2: exiting angle
    """

    def __init__(self):
        """
        Initializes equation
        """
        self.n1, self.theta1, self.n2, self.theta2 = sym.symbols("n1 theta1 n2 theta2")
        self.equation = sym.Eq(self.n1 * sym.sin(self.theta1), self.n2 * sym.sin(self.theta2))
    
    def show(self):
        """
        Shows equation
        """
        sym.pprint(self.equation)

    def solve_n1(self, theta1, n2, theta2):
        """
        Solves equation for incident index of refraction

        theta1: incident angle\n
        n2:     exiting index of refraction\n
        theta2: exiting angle
        """
        equation = self.equation.subs([(self.theta1, theta1), (self.n2, n2), (self.theta2, theta2)])
        return sym.solve(equation, self.n1)[0]
    
    def solve_theta1(self, n1, n2, theta2):
        """
        Solves equation for incident angle

        n1:     incident index of refraction\n
        n2:     exiting index of refraction\n
        theta2: exiting angle
        """
        equation = self.equation.subs([(self.n1, n1), (self.n2, n2), (self.theta2, theta2)])
        return sym.solve(equation, self.theta1)[0]
    
    def solve_n2(self, n1, theta1, theta2):
        """
        Solves equation for exiting index of refraction

        n1:     incident index of refraction\n
        theta1: incident angle\n
        theta2: exiting angle
        """
        equation = self.equation.subs([(self.n1, n1), (self.theta1, theta1), (self.theta2, theta2)])
        return sym.solve(equation, self.n2)[0]

    def solve_theta2(self, n1, theta1, n2):
        """
        Solves equation for exiting angle

        n1:     incident index of refraction\n
        theta1: incident angle\n
        n2:     exiting index of refraction
        """
        equation = self.equation.subs([(self.n1, n1), (self.theta1, theta1), (self.n2, n2)])
        return sym.solve(equation, self.theta2)[0]


if __name__ == "__main__":
    """
    Run test code here
    """

    snells_law().show()
    