# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import ndimage
import glob
import tools.detection as dt
import tools.tools as tools

def cellDist(celldf, objCent, plot, cutFarCells, searchRad):
# takes a dataframe with cell positions, and an object position
# finds distance from object, and plots for each time frame

    print('Calculating distances from object')
    # calculate distance from object
    celldf['xdiff'] = abs(celldf['x'] - objCent[1])
    celldf['ydiff'] = abs(celldf['y'] - objCent[0])
    celldf['sq'] = (celldf['xdiff'] * celldf['xdiff'] +
                    celldf['ydiff'] * celldf['ydiff'])
    celldf['objDist'] = celldf[['sq']].sum(axis=1).pow(1./2)
    
    if cutFarCells:
        # remove cells too far away
        celldf = celldf[celldf['objDist'] < searchRad]
    
    if plot:
        print('Plotting')
        sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    
        plotmax = max(celldf['objDist'])
        framemax = max(celldf['frame'])
        pal = sns.cubehelix_palette(framemax+1, rot=-.25, light=.7)
        g = sns.FacetGrid(celldf, row="frame", hue="frame", aspect=20,
                          size=.4, palette=pal)
    
        g = g.map(sns.kdeplot, "objDist",  clip_on=False, shade=True,
                  alpha=0.7, lw=1.5, bw=20).set(xlim=(0, plotmax))
        g = g.map(sns.kdeplot, "objDist",  clip_on=False, color="w",
                  lw=2, bw=20).set(xlim=(0, plotmax))
        g.map(plt.axhline, y=0, lw=1, clip_on=False)
    
        def label(x, color, label):
            ax = plt.gca()
            ax.text(0, .2, label, fontweight="bold", color=color,
                    ha="left", va="center", transform=ax.transAxes)
    
        g.map(label, "frame")
    
        # Set the subplots to overlap
        g.fig.subplots_adjust(hspace=-.4)
    
        # Remove axes details that don't play will with overlap
        g.set_titles("")
        g.set(yticks=[])
        g.set(xticks=[])
        g.set_xlabels('Distance to object')
        g.despine(bottom=True, left=True)

        plt.show(block=False)

    return celldf


def cells_in_object(celldf, obj_mask, plot, plot_smooth=False):
    print('Calculating number of cells in object')
    num_cells_in_obj = np.zeros(celldf['frame'].max() + 1)
    num_cells_total = np.zeros(celldf['frame'].max() + 1)
    area_object = np.zeros(celldf['frame'].max() + 1)


    for t in range(0, celldf['frame'].max() + 1):
        obj_indices = np.argwhere(obj_mask[t] == True)
        df = celldf[celldf['frame'] == t]
        df = df.round({'x': 0, 'y': 0})

        # get number of cells where x and y vals fall within the object
        cells_in_obj = df[df['x'].isin(obj_indices[:, 1]) &
                          df['y'].isin(obj_indices[:, 0])]

        num_cells_in_obj[t] = len(cells_in_obj)
        num_cells_total[t] = len(df)
        area_object[t] = obj_mask[t].sum()

    if plot:
        smooth_sigma = 4
        fig, ax = plt.subplots()
        x = np.arange(0, len(num_cells_in_obj))
        if plot_smooth:
            num_cells = ndimage.filters.gaussian_filter1d(
                num_cells_in_obj, smooth_sigma)

        ax.plot(x, num_cells)
        ax.set(xlabel='Time', ylabel='Number of cells')
        ax.set_title('Number of cells in object over time')

        plt.show(block=False)
    return num_cells_in_obj, num_cells_total, area_object


def analysis_run(var, opt):
    filenames = glob.glob('*C1.tif')
    movies = [Movie(file, opt, var) for file in filenames]
    return movies


class Movie:
    def __init__(self, file, opt, var):
        print('Analysing file: ', file)
        self.file = file
        self.objCent = dt.obj_cent_single(self.file, opt.plot)
        self.cellsdf = dt.cell_detect(self.file, var, opt)
        self.celldf = cellDist(self.cellsdf, self.objCent, opt.plot,
                          opt.cutFarCells, var.staticSearchRad)

        im_thresh = dt.obj_seg(file, var, opt)
        self.num_cells_in_obj, self.num_cells_total, self.area_object =\
            cells_in_object(self.celldf, im_thresh, opt.plot, plot_smooth=True)


def all_movies(movies, opt, var, direc):
    if opt.savecsv:
        tools.save_1d_csv(movies, 'file',
                          'num_cells_in_obj',
                          'num_cells_total',
                          'area_object')


