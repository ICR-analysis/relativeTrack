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
import tools.plot as plot
import pandas as pd


def cell_dist(celldf, obj_cent, plot, cut_far_cells, search_rad):
    # takes a dataframe with cell positions, and an object position
    # finds distance from object, and plots for each time frame

    print('Calculating distances from object')
    # calculate distance from object
    celldf['xdiff'] = abs(celldf['x'] - obj_cent[1])
    celldf['ydiff'] = abs(celldf['y'] - obj_cent[0])
    celldf['sq'] = (celldf['xdiff'] * celldf['xdiff'] +
                    celldf['ydiff'] * celldf['ydiff'])
    celldf['objDist'] = celldf[['sq']].sum(axis=1).pow(1./2)
    
    if cut_far_cells:
        # remove cells too far away
        celldf = celldf[celldf['objDist'] < search_rad]
    
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
    cells_in_obj = pd.DataFrame()

    for t in range(0, celldf['frame'].max() + 1):
        obj_indices = np.argwhere(obj_mask[t] == True)
        df = celldf[celldf['frame'] == t]
        df = df.round({'x': 0, 'y': 0})

        obj_indices_df = pd.DataFrame(obj_indices, columns=['y', 'x'])

        # get common rows - i.e. cells in object
        cells_in_obj_tmp = pd.merge(df, obj_indices_df, on=['x', 'y'],
                                    how='inner')

        # keep cells in obj and return
        cells_in_obj = cells_in_obj.append(cells_in_obj_tmp, ignore_index=True)

        num_cells_in_obj[t] = len(cells_in_obj_tmp)
        num_cells_total[t] = len(df)
        area_object[t] = obj_mask[t].sum()

    if plot:
        smooth_sigma = 4
        fig, ax = plt.subplots()
        x = np.arange(0, len(num_cells_in_obj))
        if plot_smooth:
            num_cells = ndimage.filters.gaussian_filter1d(
                num_cells_in_obj, smooth_sigma)
        else:
            num_cells = num_cells_in_obj

        ax.plot(x, num_cells)
        ax.set(xlabel='Time', ylabel='Number of cells')
        ax.set_title('Number of cells in object over time')

        plt.show(block=False)
    return num_cells_in_obj, num_cells_total, area_object, cells_in_obj


def analysis_run(var, opt):
    filenames = glob.glob('*C1.tif')
    movies = [Movie(file, opt, var) for file in filenames]
    return movies


class Movie:
    def __init__(self, file, opt, var):
        print('Analysing file: ', file)
        self.file = file
        self.thresh_c0, self.raw_c0 = dt.obj_seg(
            self.file.replace("C1.tif", "C0.tif"),
            thresh_adj=var['obj_thresh_adj'],
            bleach_correction=opt['bleach_correction'],
            frames_keep=var['frames_keep'],
            smooth_sigma=var['obj_thresh_smooth'],
            mult_obj=opt['mult_obj_support'],
            crop_ratio=var['crop_ratio_mult_obj'],
            plot=opt['plot_inter_static'])

        self.objCent = dt.obj_cent(self.thresh_c0, opt['plot_inter_static'])
        self.cellsdf, self.raw_frames = dt.cell_detect(self.file, var, opt)
        self.celldf = cell_dist(self.cellsdf, self.objCent,
                                opt['plot_inter_static'], opt['cutFarCells'],
                                var['staticSearchRad'])

        self.num_cells_in_obj, self.num_cells_total,\
            self.area_object, self.cells_in_obj =\
            cells_in_object(self.celldf, self.thresh_c0, opt['plot_inter_static'],
                            plot_smooth=var['cell_obj_plot_smooth'])


def all_movies(movies, opt, var, direc):
    if opt['savecsv']:
        print('Saving results as .csv')
        tools.save_1d_csv(movies, 'file',
                          'num_cells_in_obj',
                          'num_cells_total',
                          'area_object')

    if opt['save_vars']:
        print('Saving analysis options')
        tools.options_variables_write(opt, var, direc)


def plotting(movies, opt, var, movie_plot=0):
    if var['frames_keep'] is 0:
        max_t = len(movies[movie_plot].raw_frames)
    else:
        max_t = var['frames_keep']

    if opt['plot_inter_temporal']:
        print('Plotting dynamic figures')
        plot.scroll_overlay(movies[movie_plot].raw_frames,
                            movies[movie_plot].cellsdf, 'Cell segmentation',
                            cell_diameter=var['diameter'])

        plot.scroll_overlay(movies[movie_plot].raw_c0[0:max_t],
                            movies[movie_plot].cells_in_obj, 'Cells in object',
                            cell_diameter=var['diameter'], vmax=500)

        plot.scroll_overlay(movies[movie_plot].thresh_c0[0:max_t],
                            movies[movie_plot].cells_in_obj,
                            'Cells in segmented object',
                            cell_diameter=var['diameter'], vmax=1)




