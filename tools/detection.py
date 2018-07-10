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

    objim_file = file.replace("C1.tif", "C0.tif")
    obj_im = skimage.io.imread(objim_file)
    sum_proj = np.sum(obj_im, 0)
    sum_proj = np.square(sum_proj)  # weight intensity more than distance
    agnostic_mask = np.ones(
            sum_proj.shape).astype(int)  # regionprops needs a 'mask'
    obj_cent = skimage.measure.regionprops(
            agnostic_mask, sum_proj)[0]['weighted_centroid']

    if plot:
        print('Plotting')
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(sum_proj)
        circ = mpl.patches.Circle((obj_cent[1], obj_cent[0]), 50)
        ax.add_patch(circ)
        ax.set_title('Object centre')
        plt.show(block=False)

    return obj_cent


def bleach_correction_blind(im):
    bleaching = np.mean(im, (1, 2))
    bleach_corrected = im/bleaching[:, None, None]
    return bleach_corrected, bleaching


def obj_seg(file, var, opt, bleach_correction=True):
    print('Segmenting object')

    objim_file = file.replace("C1.tif", "C0.tif")
    im = skimage.io.imread(objim_file)
    if bleach_correction:
        im, bleaching_trace = bleach_correction_blind(im)

    im_otsu = var['obj_thresh_adj'] * skimage.filters.threshold_otsu(im)

    if var['frames_keep'] is 0:
        max_t = len(im)
    else:
        max_t = var['frames_keep']

    im_smooth = np.zeros((max_t, im.shape[1], im.shape[2]))

    for t in range(0, max_t):
        im_smooth[t] = ndimage.filters.gaussian_filter(
            im[t], (var['obj_thresh_smooth'], var['obj_thresh_smooth']))

    im_thresh = im_smooth > im_otsu

    if opt['plot_inter_static']:
        plots.rand_plot_compare(im[0:max_t], im_thresh, num_cols=5,
                                plotsize=3,  title='Object segmentation',
                                min_val=None, max_val=im_otsu * 2)

    return im_thresh, im


def cell_detect(file, var, opt):
    print('Detecting cells')
    # http://soft-matter.github.io/trackpy/v0.3.2/tutorial/walkthrough.html

    # load, run object detection and track (then clean up)
    raw_frames = pims.TiffStack(file, as_grey=True)  # load

    # only analyse n frames
    if var['frames_keep'] is not 0:
        raw_frames = raw_frames[0:var['frames_keep']]

    # object detect
    cellsdf = tp.batch(raw_frames,
                       var['diameter'],
                       minmass=var['minFluroMass'],
                       separation=var['separation'],
                       engine='numba',
                       max_iterations=1,
                       characterize=False,
                       noise_size=var['noise_smooth'])

    # remove brightest objects
    cellsdf = cellsdf.drop(cellsdf[cellsdf.mass > var['maxFluroMass']].index)

    if opt['plot_inter_static']:
        annotate_args = {
                        "vmin": 0,
                        "vmax": 200
                        }
        # Tweak styles
        plt.ion()
        plt.show()
        fig_dims = np.multiply(0.01, raw_frames[0].shape)
        mpl.rc('figure',  figsize=(fig_dims[1].astype(int),
                                   fig_dims[0].astype(int)))
        mpl.rc('image', cmap='gray')

        # plot final particles chosen
        plt.figure()
        tp.annotate(cellsdf[cellsdf.frame == var['frame_plot']],
                    raw_frames[var['frame_plot']],
                    imshow_style=annotate_args)
        plt.title('Particles included in analysis'
                  '(at t='+str(var['frame_plot'])+')')
        plt.draw()
        plt.pause(0.001)

    return cellsdf, raw_frames
