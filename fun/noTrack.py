# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

@author: Adam Tyson
"""

import os
import tools.detection as dt
import seaborn as sns
import matplotlib.pyplot as plt


def cellDist(celldf, objCent, plot, cutFarCells, searchRad):
# takes a dataframe with cell positions, and an object position
# finds distance from object, and plots for each time frame

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
    
    return celldf

def noTrackRun(var):
    allFiles = os.listdir('.')
    for file in allFiles:
        if file.endswith("C1.tif"):
            print('Analysing file: ', file)
            objCent = dt.obj_cent_single(file, var.plot)
            cellsF = dt.cell_detect(file, var)
            celldf = cellDist(cellsF, objCent, var.plot,
                              var.cutFarCells, var.staticSearchRad)
        

