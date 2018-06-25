# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

"""
import matplotlib.pyplot as plt
from random import randint
from matplotlib.widgets import Slider
import numpy as np

def simpleplot(img, title, plotsize):  # just to tidy up plotting
    plt.figure(figsize=(plotsize, plotsize))
    plt.imshow(img, cmap="Greys_r")
    plt.title(title)
    plt.show(block=False)


def rand_plot_compare(im1, im2, num_cols=10, plotsize=3, title=None,
                      min_val=None, max_val=None):
    # Initialize the subplot panels on top of each other
    fig, ax = plt.subplots(nrows=2, ncols=num_cols,
                           figsize=(num_cols*plotsize, 2*plotsize))
    if min_val is None:
        min_val = im1.min()
    if max_val is None:
        max_val = im1.max()

    for plot in range(0, num_cols):
        t = randint(0, im1.shape[0]-1)
        ax[0][plot].imshow(im1[t], vmin=min_val, vmax=max_val, cmap="Greys_r")
        ax[0][plot].axis('off')
        if plot is 0:
            ax[0][plot].set_title('Raw:   T='+str(t))
            ax[1][plot].set_title('Thresholded')
        else:
            ax[0][plot].set_title('T='+str(t))
        ax[1][plot].imshow(im2[t], cmap="Greys_r")
        ax[1][plot].axis('off')

    if title is not None:
        fig.suptitle(title)
        plt.show(block=False)


def plot_1D(data, plotsize, title=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(3*plotsize, 3*plotsize))
    plt.plot(data)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    plt.show(block=False)


def scroll_plot(im_in, title_in=None, figsize=(12, 16)):
    # adapted from:
    # http://www.math.buffalo.edu/~badzioch/MTH337/PT/
    # PT-matplotlib_slider/PT-matplotlib_slider.html

    global im
    im = im_in
    global title
    if title_in is None:
        title = "Image"
    else:
        title = title_in

    t_min = 0
    t_max = len(im)-1
    t_init = 0

    fig = plt.figure(figsize=figsize)

    main_ax = plt.axes([0.1, 0.2, 0.8, 0.65])
    slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
    main_ax.set_xticks([])
    main_ax.set_yticks([])

    plt.axes(main_ax)
    plt.title(title)
    main_plot = plt.imshow(im[t_init, :, :])

    t_slider = Slider(slider_ax, 'Timepoint', t_min,t_max, valfmt="%i",
                      valinit=t_init, valstep=1)

    def update(t):
        t = int(t)
        main_plot.set_data(im[t, :, :])
        fig.canvas.draw_idle()     # redraw the plot

    t_slider.on_changed(update)
    plt.show(block=False)
    # plt.show(block=True)


def scroll_overlay(im_in, points_in, title=None, figsize=(12, 16),
                   cell_diameter=25):
    # input
    # im_in - series of frames from pims
    # points in - data frame with 'x', 'y' and 'frames'
    print('Plotting segmentation')
    global im
    global points
    global scatter_plot

    im = im_in
    points = points_in
    # im = movies[0].raw_frames
    # points = movies[0].cellsdf

    if title is None:
        title = "Image"

    t_min = 0
    t_max = len(im)-1
    t_init = 0

    fig = plt.figure(figsize=figsize)

    main_ax = plt.axes([0.1, 0.2, 0.8, 0.65], )

    slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
    main_ax.set_xticks([])
    main_ax.set_yticks([])

    plt.axes(main_ax)
    plt.title(title)
    points_frame = points[points['frame'] == t_init]
    im_plot = plt.imshow(im[t_init], cmap="Greys_r", vmin=0, vmax=200)
    scatter_plot = plt.scatter(points_frame['x'] , points_frame['y'],
                               s=6*cell_diameter, edgecolors='r',
                               facecolors='none')
    t_slider = Slider(slider_ax, 'Timepoint', t_min, t_max, valfmt="%i",
                      valinit=t_init, valstep=1)

    def update(t):
        global scatter_plot
        t = int(t)
        im_plot.set_data(im[t])
        points_frame_upt = points[points['frame'] == t]
        scatter_plot.set_offsets(np.c_[(points_frame_upt['x'],
                                        points_frame_upt['y'])])
        fig.canvas.draw_idle()     # redraw the plot

    t_slider.on_changed(update)
    # plt.show(block=False)
    plt.show(block=True)
