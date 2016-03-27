import math
try:
    import numpy as np
except ImportError:
    print("\nNumpy module must be installed to use this package. Exiting.\n")
try:
    import scipy.optimize as opt
except ImportError:
    print("\nScipy module must be installed to use this package. Exiting.\n")

"""@package distributions
This module contains classes and functions for creating different types
of point distributions.  Uniform and hyperbolic tangent distributions
are currently supported.  Additional distributions could be added
relatively easily by creating new classes which have a method s(i)
for getting the intermediate spacing function.

@author James Grisham
@date 03/24/2016

"""


class Uniform:
    """Class which represents a uniform point distribution.
    """

    def __init__(self, imax):
        """Constructor.

        @param imax number of points.
        """
        self.imax = imax

    def s(self, i):
        """ Method for getting the intermediate spacing function.

        @param i coordinate for the i-th point.
        @return s(i).
        """
        return float(i)/float(self.imax)


class HyperbolicTangent:
    """Class which represents a hyperbolic tangent point distribution.

    """

    def __init__(self, imax, ds, lx=1.0, reverse=False):
        """Constructor.

        @param imax number of points.
        @param ds clustering toward beginning.
        @param lx total x-length of segment.
        @param reverse boolean variable used to reverse direction of clustering.
        """
        self.delta = 1.0
        self.imax = imax
        self.ds = ds/lx
        self.reverse = reverse
        self.s_fun = lambda d, i: 1.0 + math.tanh(d*(float(i)/float(self.imax)-1.0))/math.tanh(d)
        self.find_delta()

    def find_delta(self):
        """Method for finding delta.
        This method finds the value of delta required to match with the given ds.
        """
        f = lambda dv: math.fabs(self.ds - self.s_fun(dv, 1))
        res = opt.minimize(f, 1.0)
        self.delta = res.x[0]

    def s(self, i):
        """Method for getting the intermediate spacing function.

        @param i coordinate for the i-th point.
        @return s(i).
        """

        if not self.reverse:
            return self.s_fun(self.delta, i)
        else:
            return 1.0 - self.s_fun(self.delta, i)
