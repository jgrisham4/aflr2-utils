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
import matplotlib.pyplot as plt
from subprocess import call

# Inputs
root_name = "rae2822"
blr = 1.2
blds = 1.0e-4

# Importing geometry from file
segs = g.import_geometry("{}.seg".format(root_name))

# Dimensioning connectors
n_u0 = 100
n_u1 = 80
n_l0 = 100
n_l1 = 80

# Creating point distribution objects
d_upper0 = d.HyperbolicTangent(n_u0, 1.0e-3)
d_upper1 = d.HyperbolicTangent(n_u1, 1.0e-3)
d_lower0 = d.HyperbolicTangent(n_l0, 1.0e-3)
d_lower1 = d.HyperbolicTangent(n_l1, 1.0e-3)

# Creating connectors 
# bcs:
# 0 -> inviscid wall
# 1 -> viscous wall
# 2 -> farfield
con_upper0 = m.Connector(segs[0], n_u0, bc=1)
con_upper1 = m.Connector(segs[1], n_u1, bc=1)
con_lower0 = m.Connector(segs[2], n_l0, bc=1)
con_lower1 = m.Connector(segs[3], n_l1, bc=1)

# Creating point distributions on the connectors
con_upper0.create_point_distribution(d_upper0)
con_upper1.create_point_distribution(d_upper1, cluster_end=True)
con_lower0.create_point_distribution(d_lower0)
con_lower1.create_point_distribution(d_lower1, cluster_end=True)

# Creating farfield
con_ff = m.create_circular_connector(0.5, 0.0, 30.0, 100)
con_ff.bc = 2    # farfield bc

# Must reverse the order of the nodes on the bottom
# so that contour proceeds in a CW direction
con_lower0.nodes.reverse()
con_lower1.nodes.reverse()

# Creating edges with connectors
inner_edge = m.Edge([con_lower1, con_lower0, con_upper0, con_upper1])
outer_edge = m.Edge([con_ff])

# Creating mesh object
grid = m.Mesh([inner_edge, outer_edge])

# Writing bedge file
grid.write_bedge("{}.bedge".format(root_name))

# Calling aflr2
aflr2_command = "simcenter aflr2 -ibedge -ascii -melem 1000000 -bl -blr {} -blds {} {}".format(blr, blds, root_name)
call(aflr2_command, shell=True)

# Visualizing grid using xplt2 which was distributed with aflr2
call("simcenter xplt2 {}".format(root_name), shell=True)
