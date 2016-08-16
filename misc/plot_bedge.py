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

"""
This Python script searches for all files with the bedge extension in whatever
directory it is run from and then plots the bedge file using Matplotlib.

James Grisham
"""

import os
import sys
try:
    import numpy as np
except ImportError:
    print("\nNumpy module must be installed to use this script.  Exiting.\n")
    sys.exit()
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("\nMatplotlib module must be installed to use this script. Exiting.\n")
    sys.exit()

# Using list-comprehension to find all bedge files within the current directory
bedge_files = [f for f in os.listdir(os.getcwd()) if f.endswith(".bedge")]

# Plotting
figlist = []
ctr = 0
for f in bedge_files:
    data = np.genfromtxt(f, skip_header=4)
    figlist.append(plt.figure())
    plt.plot(data[:,0], data[:,1], "+k")
    plt.axis("equal")
    plt.xlabel("x")
    plt.ylabel("y")
    ctr += 1

plt.show()
