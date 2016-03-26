import math
import aflr2utils.geometry as g


"""@package mesh
This module contains several classes and functions
for dealing with mesh-related data.  The relevant classes
are: Connector, Edge and Mesh.  There are also functions
for creating circular connectors and circular arcs.

@author James Grisham
@date 03/24/2016

"""


def create_circular_connector(xc, yc, r, num_points):
    """Function for creating a circular connector.
    This function creates a circular connector when provided with
    the x- and y-coordinates of the center of the circle and the
    radius of the circle.  A uniform point distribution is created on
    the circle.

    @param xc x-coordinate of the center of the circle.
    @param yc y-coordinate of the center of the circle.
    @param r radius of the circle.
    @param num_points number of points on the circle.
    """
    con = Connector(None, num_points)
    dtheta = 2.0*math.pi/(float(num_points) - 1.0)
    theta = 0.0
    for i in range(0, num_points):
        xv = r*math.cos(theta) + xc
        yv = r*math.sin(theta) + yc
        theta += dtheta
        con.nodes.append(g.Point(xv, yv))

    return con


def create_circular_arc_connector(xc, yc, r, theta_start, theta_stop, num_points):
    """Function for creating a circular connector.
    This function creates a circular connector when provided with
    the x- and y-coordinates of the center of the circle and the
    radius of the circle.  A uniform point distribution is created on
    the circle.

    @param xc x-coordinate of the center of the circle.
    @param yc y-coordinate of the center of the circle.
    @param r radius of the circle.
    @param theta_start starting angle in radians.
    @param theta_stop final angle in radians.
    @param num_points number of points on the circle.
    """
    con = Connector(None, num_points)
    dtheta = (theta_stop - theta_start)/(float(num_points) - 1.0)
    theta = theta_start
    for i in range(0, num_points):
        xv = r*math.cos(theta) + xc
        yv = r*math.sin(theta) + yc
        theta += dtheta
        con.nodes.append(g.Point(xv, yv))

    return con


class Connector:
    """Class for connector (in Pointwise terminology).

    """

    def __init__(self, seg, num_points, bc=0):
        """Constructor.
        Possible boundary conditions (bc) values are
        0 - inviscid
        1 - viscous
        2 - farfield

        @param seg input segment object on which connector will be created.
        """
        self.seg = seg
        self.num_points = num_points
        self.nodes = []
        self.bc = bc

    def create_point_distribution(self, distribution, cluster_end=False):
        """Method for creating points on a connector.
        This method assumes that you want to cluster towards the start of the connector.
        If this is not the case, set cluster_end to True.

        @param distribution a point distribution object from distributions.py.
        @param cluster_end boolean variable used to control clustering direction.
        """
        self.seg.spacing_function = distribution
        self.seg.spacing_function.reverse = cluster_end
        for i in range(0, self.num_points+1):
            self.nodes.append(self.seg.get_point(i))
        if cluster_end:
            self.nodes.reverse()


class Edge:
    """Edge class which is a collection of connectors
    """

    def __init__(self, connectors):
        """Constructor.

        @param connectors list of connectors which belong to this edge.
        """
        self.connectors = connectors


class Mesh:
    """Class which represents a mesh.
    A mesh is a collection of edges which represent the boundaries.
    """

    def __init__(self, edges):
        """Constructor.

        @param edges list of edges which represent the boundaries in the mesh.
        """
        self.edges = edges

    def write_bedge(self, bedge_name):
        """Method for writing boundaries (edges) to a bedge file.
        This method writes a bedge file which is input for
        AFLR2.

        @param bedge_name string which contains the name of the output file.
        """
        with open(bedge_name, "w") as bedge_file:

            # Writing number of boundary groups
            bedge_file.write("{:5d}\n".format(len(self.edges)))

            # Writing number of connectors per edge
            # or number of boundary surfaces per group
            for e in self.edges:
                bedge_file.write("{:5d} ".format(len(e.connectors)))
            bedge_file.write("\n")

            # Writing number of nodes for each connector
            for e in self.edges:
                for c in e.connectors:
                    bedge_file.write("{:5d} ".format(len(c.nodes)-1))
            bedge_file.write("\n")

            # Writing boundary conditions
            for e in self.edges:
                for c in e.connectors:
                    bedge_file.write("{:5d} ".format(c.bc))
            bedge_file.write("\n")

            # Writing x- and y-coordinates
            for e in self.edges:
                for c in e.connectors:
                    for i in range(0, len(c.nodes)-1):
                        bedge_file.write("{:5.15f} {:5.15f}\n".format(c.nodes[i].x, c.nodes[i].y))
