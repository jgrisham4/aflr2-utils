#!/usr/bin/env python3

import aflr2utils.geometry as geom
import aflr2utils.distributions as dist
import aflr2utils.mesh as m
import matplotlib.pyplot as plt
import math
from subprocess import call

# Inputs
blr = 1.1
blds = 1.0e-5
root_name = "flatplate"
intds = 1.0e-4
imax_inv = 100
imax_visc = 250
imax4 = 70
jmax = 250

# Creating points
p1 = geom.Point(-0.5, 0.0)
p2 = geom.Point( 0.0, 0.0)
p3 = geom.Point( 2.0, 0.0)
p4 = geom.Point( 2.0, 2.0)
p5 = geom.Point(-0.5, 2.0)

# Creating segments from points
seg_inv    = geom.Segment([p1, p2], is_bezier = False)
seg_visc   = geom.Segment([p2, p3], is_bezier = False)
seg_norm_r = geom.Segment([p3, p4], is_bezier = False)
seg_ff     = geom.Segment([p4, p5], is_bezier = False)
seg_norm_l = geom.Segment([p5, p1], is_bezier = False)

# Creating point distributions
d1 = dist.HyperbolicTangent(imax_inv  , intds, lx=0.5)
d2 = dist.HyperbolicTangent(imax_visc , intds, lx=2.0)
d3 = dist.HyperbolicTangent(jmax      , blds, lx=2.0)
d4 = dist.Uniform(imax4)
d5 = dist.HyperbolicTangent(jmax      , blds, lx=2.0)

# Creating connectors
con1 = m.Connector(seg_inv    , imax_inv  , bc=1)
con2 = m.Connector(seg_visc   , imax_visc , bc=1)
con3 = m.Connector(seg_norm_r , jmax      , bc=2)
con4 = m.Connector(seg_ff     , imax4     , bc=2)
con5 = m.Connector(seg_norm_l , jmax      , bc=2)

# Creating point distributions on connectors
con1.create_point_distribution(d1, cluster_end=True)
con2.create_point_distribution(d2)
con3.create_point_distribution(d3)
con4.create_point_distribution(d4)
con5.create_point_distribution(d5, cluster_end=True)

# Creating edge and adding connectors
edge = m.Edge([con1, con2, con3, con4, con5])

# Creating mesh and adding edge
mesh = m.Mesh([edge])

# Writing bedge file
mesh.write_bedge("{}.bedge".format(root_name))

# Calling aflr2
aflr2_command = "simcenter aflr2 -ibedge -bref 20 -ascii -quad -melem 1000000 -bl -blr {} -blds {} {}".format(blr, blds, root_name)
call(aflr2_command, shell=True)

# Showing mesh
call("simcenter xplt2 {}".format(root_name), shell=True)
