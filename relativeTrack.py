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

N.B.:
    In saved .csv - total cells is those included in analysis
    i.e. those in search radius (if selected)
"""

# TODO Save distances from object per image
# TODO save plots and movies

from datetime import datetime
import matplotlib.pyplot as plt
import gui.gui as gui
import analysis.static_analysis as static_analysis
opt, var, direc = gui.gui_run()

plt.close('all')
var['frame_plot'] = 1
var['cell_obj_plot_smooth'] = False
var['movie_plot'] = 0
var['separation'] = var['diameter']  # separation of cells
if opt['test']:
    var['frames_keep'] = 5  # set to 0 to run all (needs to be > 3)
else:
    var['frames_keep'] = 0

startTime = datetime.now()

movies = static_analysis.analysis_run(var, opt)

static_analysis.all_movies(movies, opt, var, direc)

print('Total time taken: ', datetime.now() - startTime)

static_analysis.plotting(movies, opt, var, movie_plot=var['movie_plot'])
plt.show(block=True)

