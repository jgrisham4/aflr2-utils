#!/bin/bash

source ~/.bashrc

ds=1.9e-6

simcenter aflr2 -ibedge -ascii -melem 2000000 -bl -blr 1.10 -blds $ds  -bref 100 $1
cp "$1.ugrid" "$1_2d.ugrid"
simcenter aflr2 -ibedge -ascii -melem 2000000 -bl -blr 1.10 -blds $ds -bref 100 -3d 2 1.0 $1
