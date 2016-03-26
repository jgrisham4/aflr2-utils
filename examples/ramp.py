#!/usr/bin/env python

import aflr2utils.geometry as g
import aflr2utils.distributions as d
import aflr2utils.mesh as m
import matplotlib.pyplot as plt
import math
from subprocess import call

# Inputs
root_name = "ramp"
blr = 1.2
blds = 1.0e-5
L = 5.5  # length of the flat plate prior to the ramp
alpha = 12.0*math.pi/180.0
L_ramp = 7.0
h = 8.0

# Creating points
p1 = g.Point(-L-0.5, 0.0)
p2 = g.Point(-L, 0.0)
p3 = g.Point(0.0, 0.0)
p4 = g.Point(L_ramp, L_ramp*math.tan(alpha))
p5 = g.Point(L_ramp, h)
p6 = g.Point(-L-0.5, h)

# Creating segments using list of points
seg1 = g.Segment([p1, p2], is_bezier=False)
seg2 = g.Segment([p2, p3], is_bezier=False)
seg3 = g.Segment([p3, p4], is_bezier=False)
seg4 = g.Segment([p4, p5], is_bezier=False)
seg5 = g.Segment([p5, p6], is_bezier=False)
seg6 = g.Segment([p6, p1], is_bezier=False)

# Number of grid points for each connector
n1 = 50
n2 = 400
n3 = 400
n4 = 200
n5 = 80
n6 = 200

# Creating point distribution objects
d1 = d.Uniform(n1)
d2 = d.Uniform(n2)
d3 = d.Uniform(n3)
d4 = d.HyperbolicTangent(n4, blds)
d5 = d.Uniform(n5)
d6 = d.HyperbolicTangent(n6, 1.0e-4)

# Creating connectors
con1 = m.Connector(seg1, n1, bc=0)
con2 = m.Connector(seg2, n2, bc=1)
con3 = m.Connector(seg3, n3, bc=1)
con4 = m.Connector(seg4, n4, bc=2)
con5 = m.Connector(seg5, n5, bc=2)
con6 = m.Connector(seg6, n6, bc=2)

# Creating point distributions on connectors
con1.create_point_distribution(d1)
con2.create_point_distribution(d2)
con3.create_point_distribution(d3)
con4.create_point_distribution(d4)
con5.create_point_distribution(d5)
con6.create_point_distribution(d6, cluster_end=True)

# Creating edge and adding connectors
ramp_edge = m.Edge([con1, con2, con3, con4, con5, con6])

# Creating mesh and adding edge
ramp_mesh = m.Mesh([ramp_edge])

# Writing bedge file
ramp_mesh.write_bedge("{}.bedge".format(root_name))

# Calling aflr2
aflr2_command = "simcenter aflr2 -ibedge -ascii -melem 1000000 -bl -blr {} -blds {} {}".format(blr, blds, root_name)
call(aflr2_command, shell=True)

# Visualizing grid using xplt2 which was distributed with aflr2
call("simcenter xplt2 {}".format(root_name), shell=True)
