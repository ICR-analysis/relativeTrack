# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-03-05

@author: Adam Tyson

Implements Crocker & Grier's (1996) local nearest neighbour tracking by
using trackpy. Requires low densities, and low movement per frame.

INSTRUCTIONS:
    - In slidebook, calculate max projection, and export all files
      as OME-TIFF into a single directory.
    - Run relativeTrack.py and results will be saved as .csv into the same
      directory

CALCULATES:
    Mean displacement
    Displacement / "ideal" - compares to ideal track (straight to object)
    Mean angles wrt to "ideal" - as above (angle in radians)
    Object centre - calculated intensity weighted centre of mass
    Number of cells

REQUIRES:
    matplotlib
    numpy
    pandas
    tk
    trackpy (0.3.3) (& numba)
    skimage
    seaborn
"""
from datetime import datetime

import tools.tools as tl
from fun.cellTrack import trackRun
from fun.noTrack import noTrackRun


startTime = datetime.now()

"""
TO DO
%%%%%
Move track and no track into functions, tidy up
Save distances from object per image
%%%%%%%%%%%%
- separate two classes of particle
- extract parameter e.g. velocity
- assess motion as a function of distance from object
"""

# define variables
class var:
    radius = 25  # approx radius (must be odd)
    minFluroMass = 300   # minimum total fluorescence of a single object
    maxFluroMass = 100000  # maximum total fluorescence of a single object
    maxMove = 5  # largest pixel movement in a single frame
    maxGap = 4  # biggest gap to be closed
    minT = 30  # how many timepoints must a track last
    maxSubnet = 80  # default 30, increase to allow larger subnetworks (slow)
    plot = True
    savecsv = False
    cellTrack = False
    staticAnalysis = True  # analyse cells at each t individually
    mic_per_pix = 0.542
    s_per_frame = 0.00013889
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



tl.chooseDir()
#
if var.cellTrack:
    trackRun(var)


if var.staticAnalysis:
    noTrackRun(var)     

print('Total time taken: ', datetime.now() - startTime)
