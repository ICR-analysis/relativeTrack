# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-03-05

@author: Adam Tyson
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import pylab
import trackpy as tp
import pims
    

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    print('Finding angle between vectors')
    # from https://stackoverflow.com/questions/2827393/
    # angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def track_plot(file, var, opt):
    # http://soft-matter.github.io/trackpy/v0.3.2/tutorial/walkthrough.html

    tp.linking.Linker.MAX_SUB_NET_SIZE = var.maxSubnet

    # load, run object detection and track (then clean up)
    frames = pims.TiffStack(file, as_grey=True)  # load

    print('Detecting objects')
    f = tp.batch(frames, var.radius, minmass=var.minFluroMass, engine='numba',
                 max_iterations=1, characterize=False)  # object detect

    f = f.drop(f[f.mass > var.maxFluroMass].index)  # remove brightest objects

    t = tp.link_df(f, var.maxMove, memory=var.maxGap)  # track
    t1 = tp.filter_stubs(t, var.minT)  # only keep long tracks

    print('Calculating drift')
    # measure, and remove drift
    d = tp.compute_drift(t1)
    tm = tp.subtract_drift(t1.copy(), d)

    if opt.plot:
        print('Plotting')
        # Tweak styles
        FigDims = np.multiply(0.01, frames[0].shape)
        mpl.rc('figure',  figsize=(FigDims[1].astype(int),
                                   FigDims[0].astype(int)))
        mpl.rc('image', cmap='gray')

        # plot final particles chosen, and the trajectories
        plt.figure()
        tp.annotate(t1[t1['frame'] == 0], frames[0])
        plt.title('Particles included in analysis (at t=0)')
        plt.show(block=False)

        plt.figure()
        tp.plot_traj(t1)
        plt.title('Raw trajectories')
        plt.show(block=False)

        # plot drift-corrected trajectories
        plt.figure()
        tp.plot_traj(tm)
        plt.title('Drift-corrected trajectories')
        plt.show(block=False)

    return tp, tm


# parse out the tracking from trackpy into a simple change vector
def parse_tracking(tm):
    print('Calculating single motion vector')
    startXs = np.array([])
    endXs = np.array([])
    startYs = np.array([])
    endYs = np.array([])

    for i in tm.particle.unique():  # for each cell in list
        dataTmp = tm.loc[tm['particle'] == i]  # get data for each particle

        maxFrame = max(dataTmp.frame)
        minFrame = min(dataTmp.frame)

        startXstmp = dataTmp.x[minFrame]
        endXstmp = dataTmp.x[maxFrame]
        startYstmp = dataTmp.y[minFrame]
        endYstmp = dataTmp.y[maxFrame]

        startXs = np.append(startXs, startXstmp)
        endXs = np.append(endXs, endXstmp)
        startYs = np.append(startYs, startYstmp)
        endYs = np.append(endYs, endYstmp)

    return startXs, endXs, startYs, endYs


def compareRealIdealPaths(objXCorr, objYCorr,
                          startXs, startYs, xDiff, yDiff, numCells):

    print('Comparing real paths to "ideal"')
    xVecToObj = objXCorr-startXs
    yVecToObj = objYCorr-startYs
    magDiffObj = abs(xVecToObj * yVecToObj)  # magnitude of change

    anglesBetween = np.array([])
    for i in range(0, numCells-1):
        realVec = (xDiff[i], yDiff[i])
        idealVec = (xVecToObj[i], yVecToObj[i])
        angleBetween = angle_between(realVec, idealVec)
        anglesBetween = np.append(anglesBetween, angleBetween)

    return magDiffObj, anglesBetween


def msd(tm, mic_per_pix, s_per_frame, plot):
    print('Calculating mean square displacement')
    im = tp.imsd(tm, mic_per_pix, s_per_frame)
    em = tp.emsd(tm, mic_per_pix, s_per_frame)

    x = em.index.values
    y = em.values

    # calculate polynomial (quadratic)
    fitCoeff = np.polyfit(x, y, 2)  # x^2, x, c
    f = np.poly1d(fitCoeff)

    if plot:
        print('Plotting')
        x_new = np.linspace(x[0], x[-1], 50)
        y_new = f(x_new)
        fig, ax = plt.subplots()
        ax.plot(im.index, im, 'k-', alpha=0.1)  # black lines, semitransparent
        ax.set(ylabel=r'$\langle \Delta r^2 \rangle$ [$\mu$m$^2$]',
               xlabel='lag time $t$')

        plt.figure()
        plt.plot(x, y, 'o', x_new, y_new)
        pylab.title('Polynomial Fit')
        ax = plt.gca()
        plt.show(block=False)

    return fitCoeff
