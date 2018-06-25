# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-03-05


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
# TODO speed up object segmentation

# TODO try on different data

# TODO: better viewer for cell segmentation
# TODO: plot cells in spheroid (save as movie)
# TODO: option to choose which frames to plot
# TODO: find way of removing small, but bright things

# TODO: segment one central spheroid out of many

from datetime import datetime
import matplotlib.pyplot as plt
import tools.GUI as GUI
import analysis.static_analysis as static_analysis

opt, var, direc = GUI.run()
plt.close('all')
var.frame_plot = 1

if opt.test:
    var.frames_keep = 5  # set to 0 to run all (needs to be > 3)


startTime = datetime.now()

movies = static_analysis.analysis_run(var, opt)

static_analysis.all_movies(movies, opt, var, direc)

print('Total time taken: ', datetime.now() - startTime)

static_analysis.plotting(movies, opt, var)
plt.show(block=True)

