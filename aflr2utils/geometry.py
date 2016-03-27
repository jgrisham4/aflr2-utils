import os
import sys
import aflr2utils.distributions as d
try:
    import numpy as np
except ImportError:
    print("\nNumpy module must be installed to use this package. Exiting.\n")
try:
    import scipy.optimize as opt
except ImportError:
    print("\nScipy module must be installed to use this package. Exiting.\n")


"""@package geometry
This module contains several classes and functions for 
dealing with geometry.

@author James Grisham
@date 03/23/2016

"""


def import_geometry(file_name):
    """Function for importing segments from a file.

    Format of data file:
    NS
    NP_1
    x_1  y_1
    x_2  y_2
      .   .
      .   .
      .   .
    x_NP y_NP
    NC_2
    NP_1
    ...

    where
    NS   - number of segments.
    NP_i - number of knots for segment i.

    @param file_name name of file which contains data to be imported.
    @return a list of segment objects.
    """

    # Making sure file exists
    if not os.path.isfile(file_name):
        print("\n{} doesn't exist.  Exiting.\n".format(file_name))

    # Reading data
    with open(file_name) as geom_file:
        lines = geom_file.readlines()
    ns = int(lines[0])
    np = [int(lines[1])]
    print("\nImporting geometry from {} ...".format(file_name))
    print("Number of segments -> {:3d}".format(ns))
    print("Number of points for segment {:3d} -> {:4d}".format(0, np[0]))
    line_num = 2
    data = [lines[line_num:np[0]+line_num]]
    for i in range(1, ns):
        np.append(int(lines[np[i-1]+line_num]))
        print("Number of points for segment {:3d} -> {:4d}".format(i, np[-1]))
        line_num += np[i-1] + 1
        data.append(lines[line_num:np[i]+line_num])

    # Creating Point objects
    segments = []
    for d in data:
        point_list = []
        for l in d:
            lss = l.strip().split()
            xv = float(lss[0])
            yv = float(lss[1])
            point_list.append(Point(xv, yv))
        segments.append(Segment(point_list))

    print("Done importing geometry.\n")

    return segments


class Point:
    """Class which represents a point in 2D.

    """

    def __init__(self, xc, yc):
        """Constructor.

        @param xc x-coordinate of point.
        @param yc y-coordinate of point.
        """
        self.x = xc
        self.y = yc


class Segment:
    """Class which represents a line segment.

    This class represents a line segment via control points.  If only two
    control points are used, the segment is assumed to be straight.  Otherwise,
    the other supported option is for a line with four control points.  In this
    case, the segment is represented using a cubic Bezier curve.
    """

    def __init__(self, points, spacing_function=None, is_bezier=True):
        """
        This constructor must be called with a list which contains points.

        @param points list of Point objects.
        @param spacing_function optional distribution object used in fitting Bezier curve to data.
        @param is_bezier boolean variable used to switch between straight line segments and Bezier curves.
        """

        self.points = points
        self.is_bezier = is_bezier
        self.spacing_function = spacing_function
        self.bezier_fun_x = lambda i: self.p0.x*(1.0 - self.spacing_function.s(i))**3 + \
                 3.0*self.p1.x*self.spacing_function.s(i)*(1.0-self.spacing_function.s(i))**2 + \
                 3.0*self.p2.x*self.spacing_function.s(i)**2*(1.0 - self.spacing_function.s(i)) + \
                 self.p3.x*self.spacing_function.s(i)**3
        self.bezier_fun_y = lambda i: self.p0.y*(1.0 - self.spacing_function.s(i))**3 + \
                 3.0*self.p1.y*self.spacing_function.s(i)*(1.0-self.spacing_function.s(i))**2 + \
                 3.0*self.p2.y*self.spacing_function.s(i)**2*(1.0 - self.spacing_function.s(i)) + \
                 self.p3.y*self.spacing_function.s(i)**3
        self.straight_fun_x = lambda i: self.spacing_function.s(i)*(self.p1.x - self.p0.x) + self.p0.x
        self.straight_fun_y = lambda i: self.spacing_function.s(i)*(self.p1.y - self.p0.y) + self.p0.y

        # Checking to see if segment is represented as a bezier curve or a straight line
        if self.is_bezier:

            # Setting first and last control points to first and last knots
            self.p0 = points[0]
            self.p1 = Point(None, None)
            self.p2 = Point(None, None)
            self.p3 = points[-1]

            # Fixing the x-coordinates of the inner control points
            x10 = (self.p3.x - self.p0.x)/3.0 + self.p0.x
            x20 = 2.0*(self.p3.x - self.p0.x)/3.0 + self.p0.x
            y10 = (self.p3.y - self.p0.y)/3.0 + self.p0.y
            y20 = 2.0*(self.p3.y - self.p0.y)/3.0 + self.p0.y
            self.x0 = np.array([x10, y10, x20, y20])

            # Getting x and y points
            self.x_data = np.array([p.x for p in self.points])
            self.y_data = np.array([p.y for p in self.points])

            if self.spacing_function is None:
                self.spacing_function = d.Uniform(len(self.points))
            self.find_inner_control_points()

        else:

            # Must be a straight segment
            self.p0 = points[0]
            self.p1 = points[-1]

    def find_inner_control_points(self):
        """Utility function for finding the inner control points.
        """
        res = opt.minimize(self.obj_func, self.x0)
        self.p1.x = res.x[0]
        self.p1.y = res.x[1]
        self.p2.x = res.x[2]
        self.p2.y = res.x[3]


    def obj_func(self, y):
        """Objective function used in fitting the curve to the data points.

        @param y numpy array with two entries which represent y-coordinates of control pts.
        @return Sum of squares error between curve and data.
        """
        self.p1.x = y[0]
        self.p1.y = y[1]
        self.p2.x = y[2]
        self.p2.y = y[3]
        pts = [self.get_point(i) for i in range(0, len(self.points))]
        x_pts = np.array([p.x for p in pts])
        y_pts = np.interp(x_pts, self.x_data, self.y_data)
        return sum([(pts[i].y - y_pts[i])**2 for i in range(0, len(pts))])

    def get_point(self, i):
        """Method for getting the i-th point on a line.

        @param i coordinate in the computational plane (i.e., the i-th point)
        @return a Point object which has the x- and y-coordinates of the i-th point.
        """

        # Making sure spacing function has been specified
        if self.spacing_function is None:
            print("\nError: The spacing function must be specified in the segment object")
            print("prior to calling get_point().")
            print("Exiting.\n")
            sys.exit()

        if self.is_bezier:
            return Point(self.bezier_fun_x(i), self.bezier_fun_y(i))
        else:
            return Point(self.straight_fun_x(i), self.straight_fun_y(i))
