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
# TODO speed up object segmentation

# TODO save results
# TODO try on different data

# TODO: better viewer for cell segmentation
# TODO: plot cells in spheroid (save as movie)
# TODO: save cell numbers in each time pount
#


from datetime import datetime

import matplotlib.pyplot as plt

import tools.GUI as GUI
from fun.noTrack import noTrackRun

opt, var = GUI.run()
plt.close('all')

if opt.test:
    var.radius = 25  # approx radius (must be odd)
    var.minFluroMass = 300 # minimum total fluorescence of a single object
    var.maxFluroMass = 500000  # maximum total fluorescence of a single object
    var.staticSearchRad = 500  # Radius to analyse for static analysis
    var.frame_plot = 1
    var.frames_keep = 5  # set to 0 to run all (needs to be > 3)


startTime = datetime.now()
# celldf, im_thresh, num_cells = noTrackRun(var, opt
movies = noTrackRun(var, opt)






print('Total time taken: ', datetime.now() - startTime)
plt.show(block=True)

