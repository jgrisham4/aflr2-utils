#!/usr/bin/env python

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
