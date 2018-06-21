# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

"""
import matplotlib.pyplot as plt
from random import randint

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

