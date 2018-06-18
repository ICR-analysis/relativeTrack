# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

@author: Adam Tyson
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import skimage.io
import skimage.measure
import trackpy as tp
import pims


def obj_cent_single(file, plot):
    print('Finding object centre')
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
        print('Plotting')
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(sumProj)
        circ = mpl.patches.Circle((objCent[1], objCent[0]), 50)
        ax.add_patch(circ)
        plt.show(block=False)

    return objCent


def cell_detect(file, var, opt):
    print('Detecting cells')
    # http://soft-matter.github.io/trackpy/v0.3.2/tutorial/walkthrough.html

    # load, run object detection and track (then clean up)
    frames = pims.TiffStack(file, as_grey=True)  # load

    f = tp.batch(frames, var.radius, minmass=var.minFluroMass, engine='numba',
                 max_iterations=1, characterize=False)  # object detect

    f = f.drop(f[f.mass > var.maxFluroMass].index)  # remove brightest objects

    if opt.plot:
        # Tweak styles
        plt.ion()
        plt.show()
        FigDims = np.multiply(0.01, frames[0].shape)
        mpl.rc('figure',  figsize=(FigDims[1].astype(int),
                                   FigDims[0].astype(int)))
        mpl.rc('image', cmap='gray')

        # plot final particles chosen, and the trajectories
        plt.figure()
        tp.annotate(f, frames[0])
        plt.title('Particles included in analysis (at t=0)')
        # plt.show(block=False)
        plt.draw()
        plt.pause(0.001)
        # plt.show(block=False)

    return f
