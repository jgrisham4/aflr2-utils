#!/usr/bin/env python

"""
This Python script imports all segment files from whatever directory it is run from.
After importing, the segments are plotted using matplotlib.

Author: James Grisham
Date  : 12/19/2015
"""

import os
import sys
try:
    import numpy as np
except ImportError:
    print("\nNumpy module must be installed to use this script.  Exiting.\n")
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("\nMatplotlib module must be installed to use this script. Exiting.\n")

# Function for importing data from segment files
def import_seg(fname):
    with open(fname, "r") as sf:
        lines = sf.readlines()[2:]
    x = []
    y = []
    xa = []
    ya = []
    d  = False
    for l in lines:
        lsp = l.strip().split()
        #print(l)
        if len(lsp) == 2:
            x.append(float(lsp[0]))
            y.append(float(lsp[1]))
            d = True
        elif len(lsp) == 1 and d == True:
            xa.append(x)
            ya.append(y)
            x = []
            y = []
            d = False

    return (xa, ya)

# Getting list of files
seg_files = [f for f in os.listdir(os.getcwd()) if f.endswith(".seg")]

# Plotting
ls = ["-+", "--+", "-.+", ":+"]
lc = ["k", "r", "b", "g", "m", "y", "c"]
mstyle = []
for lsi in ls:
    for lci in lc:
        mstyle.append("{}{}".format(lsi, lci))

for f in seg_files:
    xpts, ypts = import_seg(f)
    plt.figure()
    for i in range(0, len(xpts)):
        plt.plot(xpts[i], ypts[i], "{}".format(mstyle[i]), lw=1.5, label="{}".format(i))
    plt.axis("equal")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")

plt.show()

