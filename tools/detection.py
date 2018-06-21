# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pims
import skimage.filters
import skimage.io
import skimage.measure
import trackpy as tp
from scipy import ndimage

import tools.plot as plots


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
        ax.set_title('Object centre')

        plt.show(block=False)

    return objCent


def obj_seg(file, var, opt):
    print('Segmenting object')

    objim_file = file.replace("C1.tif", "C0.tif")
    im = skimage.io.imread(objim_file)
    im_otsu = var.obj_thresh_adj * skimage.filters.threshold_otsu(im)

    if var.frames_keep is 0:
        max_t = len(im)
    else:
        max_t = var.frames_keep

    im_smooth = np.zeros((max_t, im.shape[1], im.shape[2]))

    for t in range(0, max_t):
        im_smooth[t] = ndimage.filters.gaussian_filter(
            im[t], (var.obj_thresh_smooth, var.obj_thresh_smooth))

    im_thresh = im_smooth > im_otsu

    if opt.plot:
        plots.rand_plot_compare(im[0:max_t], im_thresh, num_cols=5,
                                plotsize=3,  title='Object segmentation',
                                min_val=None, max_val=im_otsu * 2)

    return im_thresh


def cell_detect(file, var, opt):
    print('Detecting cells')
    # http://soft-matter.github.io/trackpy/v0.3.2/tutorial/walkthrough.html

    # load, run object detection and track (then clean up)
    frames = pims.TiffStack(file, as_grey=True)  # load

    # only analyse n frames
    if var.frames_keep is not 0:
        frames = frames[0:var.frames_keep]

    f = tp.batch(frames, var.radius, minmass=var.minFluroMass,
                 separation=var.separation, engine='numba',
                 max_iterations=1, characterize=False)  # object detect

    f = f.drop(f[f.mass > var.maxFluroMass].index)  # remove brightest objects

    if opt.plot:
        annotate_args = {
                        "vmin" : 0,
                        "vmax" : 200
                        }
        # Tweak styles
        plt.ion()
        plt.show()
        FigDims = np.multiply(0.01, frames[0].shape)
        mpl.rc('figure',  figsize=(FigDims[1].astype(int),
                                   FigDims[0].astype(int)))
        mpl.rc('image', cmap='gray')

        # plot final particles chosen
        plt.figure()
        tp.annotate(f[f.frame == var.frame_plot], frames[var.frame_plot],
                    imshow_style=annotate_args)
        plt.title('Particles included in analysis'
                  '(at t='+str(var.frame_plot)+')')
        # plt.show(block=False)
        plt.draw()
        plt.pause(0.001)
        # plt.show(block=False)

    return f
