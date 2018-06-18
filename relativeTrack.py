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
    pims
"""

# TODO Save distances from object per image
# TODO make parallel with ipyparallel?
# TODO remove objects that dont move
# TODO option to only analyse n frames
# TODO count cells only in object

from datetime import datetime
from fun.noTrack import noTrackRun
import matplotlib.pyplot as plt
import tools.GUI as GUI
from tools.detection import obj_seg



opt, var = GUI.run()
plt.close('all')
var.separation = 27
var.obj_thresh_adj = 0.8
var.obj_thresh_smooth = 50
if opt.test:
    var.radius = 25  # approx radius (must be odd)
    var.minFluroMass = 800  # minimum total fluorescence of a single object
    var.maxFluroMass = 50000  # maximum total fluorescence of a single object
    var.staticSearchRad = 500  # Radius to analyse for static analysis
    var.frame_plot = 1
    var.frames_keep = 5  # set to 0 to run all (needs to be > 3)

# file = 'E:\\Adam\\MariaTrack\\analyse-2018-06-05\R1029_1\\' \
#        'Capture 2 - D4_1_29_IFNg_CEA.Project Maximum Z_' \
#        'XY1526059416_Z0_T00_C1.tif'



# obj_seg(file, var, opt)
# plt.show(block=True)



startTime = datetime.now()
noTrackRun(var, opt)
print('Total time taken: ', datetime.now() - startTime)
plt.show(block=True)

