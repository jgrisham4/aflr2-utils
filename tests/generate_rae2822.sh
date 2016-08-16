#!/bin/bash

# This file is part of aflr2-utils.
# 
# aflr2-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# aflr2-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with aflr2-utils.  If not, see <http://www.gnu.org/licenses/>.

source ~/.bashrc

ds=1.0e-4

simcenter aflr2 -ibedge -ascii -melem 2000000 -bl -blr 1.10 -blds $ds  -bref 100 $1
#cp "$1.ugrid" "$1_2d.ugrid"
#simcenter aflr2 -ibedge -ascii -melem 2000000 -bl -blr 1.10 -blds $ds -bref 100 -3d 2 1.0 $1
