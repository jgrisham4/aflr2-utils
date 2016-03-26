#!/usr/bin/env python

import aflr2utils.geometry as g
import aflr2utils.distributions as d
import aflr2utils.mesh as m

# Importing geometry from file
segs = g.import_geometry("rae2822.seg")

# Dimensioning connectors
n_u0 = 100
n_u1 = 80
n_l0 = 100
n_l1 = 80

# Creating point distribution object
d_upper0 = d.HyperbolicTangent(n_u0, 1.0e-3)
d_upper1 = d.HyperbolicTangent(n_u1, 1.0e-3)
d_lower0 = d.HyperbolicTangent(n_l0, 1.0e-3)
d_lower1 = d.HyperbolicTangent(n_l1, 1.0e-3)

# Creating connectors
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

# Creating edges
inner_edge = m.Edge([con_lower1, con_lower0, con_upper0, con_upper1])
outer_edge = m.Edge([con_ff])

# Creating mesh objects
grid = m.Mesh([inner_edge, outer_edge])
grid.write_bedge("airfoil.bedge")

