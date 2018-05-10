# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

@author: Adam Tyson
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import skimage.io
import skimage.measure
import trackpy as tp
import pims


def obj_cent(file, plot):
    # takes the C1 file, and loads the C0 file
    # finds the intensity weighted centroid
    # maybe plots


    objim_file = file.replace("C1.tif", "C0.tif")
    objIm = skimage.io.imread(objim_file)
    sumProj = np.sum(objIm, 0)
    sumProj = np.square(sumProj)  # weight intensity more than distance
    agnosticMask = np.ones(
            sumProj.shape).astype(int)  # regionprops needs a 'mask'
    objCent = skimage.measure.regionprops(
            agnosticMask, sumProj)[0]['weighted_centroid']

    if plot:
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(sumProj)
        circ = mpl.patches.Circle((objCent[1], objCent[0]), 50)
        ax.add_patch(circ)
        plt.show()

    return objCent


def cell_detect(file, var):
    # http://soft-matter.github.io/trackpy/v0.3.2/tutorial/walkthrough.html

    # load, run object detection and track (then clean up)
    frames = pims.TiffStack(file, as_grey=True)  # load

    f = tp.batch(frames, var.radius, minmass=var.minFluroMass, engine='numba',
                 max_iterations=1, characterize=False)  # object detect

    f = f.drop(f[f.mass > var.maxFluroMass].index)  # remove brightest objects

    if var.plot:
        # Tweak styles
        FigDims = np.multiply(0.01, frames[0].shape)
        mpl.rc('figure',  figsize=(FigDims[1].astype(int),
                                   FigDims[0].astype(int)))
        mpl.rc('image', cmap='gray')

    return f

def cellDist(celldf, objCent, plot):
    # takes a dataframe with cell positions, and an object position
    # finds distance from object, and plots for each time frame

    celldf['xdiff'] = abs(celldf['x'] - objCent[1])
    celldf['ydiff'] = abs(celldf['y'] - objCent[0])
    celldf['sq'] = (celldf['xdiff'] * celldf['xdiff'] +
                    celldf['ydiff'] * celldf['ydiff'])
    celldf['objDist'] = celldf[['sq']].sum(axis=1).pow(1./2)

    if plot:
        sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

        plotmax = max(celldf['objDist'])
        framemax = max(celldf['frame'])
        pal = sns.cubehelix_palette(framemax+1, rot=-.25, light=.7)
        g = sns.FacetGrid(celldf, row="frame", hue="frame", aspect=20,
                          size=.4, palette=pal)

        g = g.map(sns.kdeplot, "objDist",  clip_on=False, shade=True,
                  alpha=0.7, lw=1.5, bw=30).set(xlim=(0, plotmax))
        g = g.map(sns.kdeplot, "objDist",  clip_on=False, color="w",
                  lw=2, bw=35).set(xlim=(0, plotmax))
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

    return celldf
