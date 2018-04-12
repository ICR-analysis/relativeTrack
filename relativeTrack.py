# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-03-05

@author: Adam Tyson

Implements Crocker & Grier's (1996) local nearest neighbour tracking by
using trackpy. Requires low densities, and low movement per frame.

INSTRUCTIONS:
    - In slidebook, calculate max projection, and export all files
      as OME-TIFF into a single directory.
    - Run relativeTrack.py and results will be saved as .csv into the same
      directory

CALCULATES:
    Mean displacement
    Displacement / "ideal" - compares to ideal track (straight to object)
    Mean angles wrt to "ideal" - as above (angle in radians)
    Object centre - calculated intensity weighted centre of mass
    Number of cells
"""
import matplotlib.pyplot as plt
import relativeTrackFuncs as tctf
import os
from datetime import datetime
import numpy as np
import pandas as pd
import tkinter
import tkinter.filedialog

startTime = datetime.now()

"""
TO DO
%%%%%
Can't track accurately - detect at each time, joyplots at each time
 of distances from object
%%%%%%%%%%%%
- separate two classes of particle
- extract parameter e.g. velocity
- assess motion as a function of distance from object
"""


# define variables
class var:
    radius = 25  # approx radius (must be odd)
    minFluroMass = 300   # minimum total fluorescence of a single object
    maxFluroMass = 100000  # maximum total fluorescence of a single object
    maxMove = 5  # largest pixel movement in a single frame
    maxGap = 4  # biggest gap to be closed
    minT = 30  # how many timepoints must a track last
    maxSubnet = 80  # default 30, increase to allow larger subnetworks (slow)
    plot = True
    savecsv = True
    mic_per_pix = 0.542
    s_per_frame = 0.00013889


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# choose a directory and move into it
root = tkinter.Tk()
root.withdraw()
imDir = tkinter.filedialog.askdirectory(title='Select image directory')

plt.close('all')
os.chdir(imDir)

if var.savecsv:
    # initialise variables
    c1Files = []
    magRatioMean = np.array([])
    magDiffMean = np.array([])
    meanAngBetween = ([])
    objCentresX = np.array([])
    objCentresY = np.array([])
    cellNumbers = np.array([])
    fit_x2 = np.array([])
    fit_x = np.array([])
    fit_c = np.array([])

allFiles = os.listdir('.')
for file in allFiles:
    if file.endswith("C1.tif"):
        print('Analysing file: ', file)

        tptm = tctf.track_plot(file, var)
        tp = tptm[0]
        tm = tptm[1]

        # Parse and analyse
        startXs, endXs, startYs, endYs = tctf.parse_tracking(tm)
        xDiff = endXs-startXs
        yDiff = endYs-startYs
        magDiff = abs(xDiff * yDiff)  # magnitude of change

        # get object centre
        objCent = tctf.obj_cent(file, var.plot)

        # get "ideal" movement vec (if particles moved directly to object)
        numCells = magDiff.size

        # check X & Y wrt row/column
        magDiffobj, anglesBetween = tctf.compareRealIdealPaths(
                objCent[1], objCent[0], startXs,
                startYs, xDiff, yDiff, numCells)

        magRatio = magDiff / magDiffobj

        msdFitCoeff = tctf.msd(tm, var.mic_per_pix,
                               var.s_per_frame, var.plot)

        print(numCells, 'particles analysed')

        if var.savecsv:
            # append variables
            c1Files.append(file)
            magDiffMean = np.append(magDiffMean, np.mean(magDiff))
            magRatioMean = np.append(magRatioMean, np.mean(magRatio))
            meanAngBetween = np.append(meanAngBetween, np.mean(anglesBetween))
            objCentresX = np.append(objCentresX, objCent[1])
            objCentresY = np.append(objCentresY, objCent[0])
            cellNumbers = np.append(cellNumbers, numCells)
            fit_x2 = np.append(fit_x2, msdFitCoeff[0])
            fit_x = np.append(fit_x, msdFitCoeff[1])
            fit_c = np.append(fit_c, msdFitCoeff[2])

if var.savecsv:
    resultsFile = "Results_" + timestamp + ".csv"
    filenames = {'Filenames': c1Files}
    df_results = pd.DataFrame(data=filenames)
    df_results['Mean displacement'] = magDiffMean
    df_results['Displacement / "ideal"'] = magRatioMean
    df_results['Mean angles wrt to "ideal"'] = meanAngBetween
    df_results['Object x coordinate'] = objCentresX
    df_results['Object y coordinate'] = objCentresY
    df_results['Number of cells'] = cellNumbers
    df_results['Polynomial fit (x^2 term)'] = fit_x2
    df_results['Polynomial fit (x term)'] = fit_x
    df_results['Polynomial fit (c term)'] = fit_c

    df_results.to_csv(resultsFile, encoding='utf-8', index=False)

print('Total time taken: ', datetime.now() - startTime)
