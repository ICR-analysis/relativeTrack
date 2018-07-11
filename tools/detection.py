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
from scipy import stats


def obj_cent(binary_im, plot=False):
    print('Finding object centre')
    # takes a binary image of an object, and returns its centre
    # assumed doesnt move (i.e. finds a single centre)
    max_proj = np.max(binary_im, 0)
    agnostic_mask = np.ones(
            max_proj.shape).astype(int)  # regionprops needs a 'mask'
    obj_centre = skimage.measure.regionprops(
            agnostic_mask, max_proj)[0]['centroid']

    if plot:
        print('Plotting')
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(max_proj)
        circ = mpl.patches.Circle((obj_centre[1], obj_centre[0]), 50)
        ax.add_patch(circ)
        ax.set_title('Object centre')
        plt.show(block=False)

    return obj_centre


def bleach_correction_blind(im):
    bleaching = np.mean(im, (1, 2))
    bleach_corrected = im/bleaching[:, None, None]
    return bleach_corrected, bleaching


def obj_seg(file, thresh_adj=1, bleach_correction=True,
            frames_keep=0, smooth_sigma=40, plot=False,
            mult_obj=False, crop_ratio=0):
    print('Segmenting object')

    # objim_file = file.replace("C1.tif", "C0.tif")
    im = skimage.io.imread(file)
    if bleach_correction:
        im, bleaching_trace = bleach_correction_blind(im)

    im_otsu = thresh_adj * skimage.filters.threshold_otsu(im)

    if frames_keep is 0:
        max_t = len(im)
    else:
        max_t = frames_keep

    im_smooth = np.zeros((max_t, im.shape[1], im.shape[2]))

    for t in range(0, max_t):
        im_smooth[t] = ndimage.filters.gaussian_filter(
            im[t], (smooth_sigma, smooth_sigma))

    im_thresh = im_smooth > im_otsu

    # find single, largest object (maybe only in centre)
    if mult_obj:
        if crop_ratio is not 0:
            start_y = int(round(im.shape[1]*((1-crop_ratio)/2)))
            end_y = int(round(im.shape[1] * (0.5+(crop_ratio/2))))
            start_x = int(round(im.shape[2]*((1-crop_ratio)/2)))
            end_x = int(round(im.shape[2] * (0.5+(crop_ratio/2))))

            mask = np.full(im_thresh.shape, False, dtype=bool)
            mask[:, start_y:end_y, start_x:end_x] = True
            im_thresh[~mask] = False

        im_thresh_single = np.full(im_thresh.shape, False, dtype=bool)
        for t in range(0, max_t):
            label_image = skimage.measure.label(im_thresh[t])
            # mode returns the smallest if >1 value
            mode = stats.mode(label_image[label_image > 0], axis=None)
            im_thresh_single[t] = label_image == mode[0]

        im_thresh = im_thresh_single

    if plot:
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
