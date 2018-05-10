# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

@author: Adam Tyson
"""
import matplotlib.pyplot as plt
import tkinter
import tkinter.filedialog
import os

def simpleplot(img, title, plotsize):  # just to tidy up plotting
    plt.figure(figsize=(plotsize, plotsize))
    plt.imshow(img, cmap="Greys_r")
    plt.title(title)

def chooseDir():
    # choose a directory and move into it
    root = tkinter.Tk()
    root.withdraw()
    imDir = tkinter.filedialog.askdirectory(title='Select image directory')
    plt.close('all')
    os.chdir(imDir)
    