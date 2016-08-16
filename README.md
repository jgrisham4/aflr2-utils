aflr2-utils-0.9
===================
aflr2-utils is a collection of Python tools meant to ease the AFLR2
mesh generation process.  The module features an object-oriented
representation of the geometry and grid.  Geometry can be created
inside a script or it can be imported from a file.  The file format
is explained in the documentation.  The terminology used is similar 
to the terminology used within Pointwise.

Prerequisites:
-------------------
The code is dependent upon Numpy and Scipy.  The code has been tested
with Python 2.7 and Python 3.4.  Some scripts in the misc directory
use Matplotlib for plotting.  The easiest way to take care of 
these dependencies is to install a Python distribution which already
includes these packages.  For example, see the free Anaconda Python
distribution here: https://www.continuum.io/downloads


Installation:
-------------------
The easiest way to install this module is to add the directory
in which this file resides to your PYTHONPATH environment variable.
This package has only been tested on Linux systems, but it should
work with Mac and Windows operating systems. 

Features:
-------------------
 - Object-oriented representation of geometric and grid entities.
 - Cubic Bezier curves for geometry.
 - Hyperbolic tangent and uniform point distributions.
 - bedge output which is required by AFLR2.

 Outline of the process:
  1. Create point objects (or import segments directly from file).
  2. Create point distributions.
  3. Create connector objects from segments and point distributions.
  4. Create an edge object for each edge and add connectors.
  5. Create a mesh object and add edges.
  6. Write .bedge file and call AFLR2.

License:
-------------------
Distributed under GNU GPLv3.  

Documentation:
-------------------
The code is documented via docstrings and manuals in PDF and HTML form
are available via Doxygen.  See the docs subdirectory.  The documentation
will be further improved before version 1.0.

Alternatively, you can view the documentation for a module, class or
function by typing >>> help(aflr2utils.module_name) in a Python interpreter
(assuming you have already imported aflr2utils.module_name).  

