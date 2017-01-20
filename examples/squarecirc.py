#!/usr/bin/env python

"""
This file is part of aflr2-utils.

aflr2-utils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

aflr2-utils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with aflr2-utils.  If not, see <http://www.gnu.org/licenses/>.
"""

import aflr2utils.geometry as g
import aflr2utils.distributions as d
import aflr2utils.mesh as m
#import matplotlib.pyplot as plt
import math
from subprocess import call

# Inputs
root_name = "mesh1"

# Creating points
p1 = g.Point(-2.0, -2.0)
p2 = g.Point(2.0, -2.0)
p3 = g.Point(2.0, 2.0)
p4 = g.Point(-2.0, 2.0)

# Creating outer boundary
seg1 = g.Segment([p1, p2], is_bezier=False)
seg2 = g.Segment([p2, p3], is_bezier=False)
seg3 = g.Segment([p3, p4], is_bezier=False)
seg4 = g.Segment([p4, p1], is_bezier=False)

# Number of grid points for each connector
#n_o = 30   # These are for mesh0
#n_i = 40
n_o = 18   # These are for mesh1
n_i = 25

# Creating inner boundary
con_inner = m.create_circular_connector(0.0, 0.0, 0.5, n_i)

# Creating point distribution objects
d1 = d.Uniform(n_o)
d2 = d.Uniform(n_o)
d3 = d.Uniform(n_o)
d4 = d.Uniform(n_o)

# Creating connectors
con1 = m.Connector(seg1, n_o, bc=0)
con2 = m.Connector(seg2, n_o, bc=1)
con3 = m.Connector(seg3, n_o, bc=1)
con4 = m.Connector(seg4, n_o, bc=2)

# Creating point distributions on connectors
con1.create_point_distribution(d1)
con2.create_point_distribution(d2)
con3.create_point_distribution(d3)
con4.create_point_distribution(d4)

# Creating edge and adding connectors
outer_edge = m.Edge([con1, con2, con3, con4])
inner_edge = m.Edge([con_inner])

# Creating mesh and adding edge
circsqu_mesh = m.Mesh([outer_edge, inner_edge])

# Writing bedge file
circsqu_mesh.write_bedge("{}.bedge".format(root_name))

# Calling aflr2
aflr2_command = "simcenter aflr2 -ibedge -fgrid -ascii {}".format(root_name)
call(aflr2_command, shell=True)

# Visualizing grid using xplt2 which was distributed with aflr2
call("simcenter xplt2 {}".format(root_name), shell=True)
