# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-03-05

@author: Adam Tyson
"""


def simpleplot(img, title, plotsize):  # just to tidy up plotting
    import matplotlib.pyplot as plt
    plt.figure(figsize=(plotsize, plotsize))
    plt.imshow(img, cmap="Greys_r")
    plt.title(title)


def unit_vector(vector):
    import numpy as np
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    # from https://stackoverflow.com/questions/2827393/
    # angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    import numpy as np
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


def track_plot(file, var):
    # http://soft-matter.github.io/trackpy/v0.3.2/tutorial/walkthrough.html
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    import pims
    import trackpy as tp

    tp.linking.Linker.MAX_SUB_NET_SIZE = var.maxSubnet

    # load, run object detection and track (then clean up)
    frames = pims.TiffStack(file, as_grey=True)  # load

    f = tp.batch(frames, var.radius, minmass=var.minFluroMass, engine='numba',
                 max_iterations=1, characterize=False)  # object detect

    f = f.drop(f[f.mass > var.maxFluroMass].index)  # remove brightest objects

    t = tp.link_df(f, var.maxMove, memory=var.maxGap)  # track
    t1 = tp.filter_stubs(t, var.minT)  # only keep long tracks

    # measure, and remove drift
    d = tp.compute_drift(t1)
    tm = tp.subtract_drift(t1.copy(), d)

    if var.plot:
        # Tweak styles
        FigDims = np.multiply(0.01, frames[0].shape)
        mpl.rc('figure',  figsize=(FigDims[1].astype(int),
                                   FigDims[0].astype(int)))
        mpl.rc('image', cmap='gray')

        # plot final particles chosen, and the trajectories
        plt.figure()
        tp.annotate(t1[t1['frame'] == 0], frames[0])
        plt.title('Particles included in analysis (at t=0)')

        plt.figure()
        tp.plot_traj(t1)
        plt.title('Raw trajectories')

        # plot drift-corrected trajectories
        plt.figure()
        tp.plot_traj(tm)
        plt.title('Drift-corrected trajectories')

    return tp, tm


# parse out the tracking from trackpy into a simple change vector
def parse_tracking(tm):
    import numpy as np
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
    import numpy as np
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


def obj_cent(file, plot):
    # takes the C1 file, and loads the C0 file
    # finds the intensity weighted centroid
    # maybe plots

    import skimage.io
    import skimage.measure
    import numpy as np
    import matplotlib.patches
    import matplotlib.pyplot as plt
    objim_file = file.replace("C1.tif", "C0.tif")
    objIm = skimage.io.imread(objim_file)
    sumProj = np.sum(objIm, 0)
    sumProj = np.square(sumProj)  # weight intensity more than distance
    agnosticMask = np.ones(
            sumProj.shape).astype(int)  # regionprops needs a 'mask'
    objCent = skimage.measure.regionprops(
            agnosticMask, sumProj)[0]['weighted_centroid']

    if plot:
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        ax.imshow(sumProj)
        circ = matplotlib.patches.Circle((objCent[1], objCent[0]), 50)
        ax.add_patch(circ)
        plt.show()

    return objCent


def msd(tm, mic_per_pix, s_per_frame, plot):
    import trackpy as tp
    import matplotlib.pyplot as plt
    from matplotlib import pylab
    import numpy as np
    im = tp.imsd(tm, mic_per_pix, s_per_frame)
    em = tp.emsd(tm, mic_per_pix, s_per_frame)

    x = em.index.values
    y = em.values

    # calculate polynomial (quadratic)
    fitCoeff = np.polyfit(x, y, 2)  # x^2, x, c
    f = np.poly1d(fitCoeff)

    if plot:
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

    return fitCoeff


def cell_detect(file, var):
    # http://soft-matter.github.io/trackpy/v0.3.2/tutorial/walkthrough.html
    import matplotlib as mpl
    import numpy as np
    import pims
    import trackpy as tp

    # load, run object detection and track (then clean up)
    frames = pims.TiffStack(file, as_grey=True)  # load

    f = tp.batch(frames, var.radius, minmass=var.minFluroMass, engine='numba',
                 max_iterations=1, characterize=False)  # object detect

    f = f.drop(f[f.mass > var.maxFluroMass].index)  # remove brightest objects

    if var.plot:
        # Tweak styles
        FigDims = np.multiply(0.01, frames[0].shape)
        mpl.rc('figure',  figsize=(FigDims[1].astype(int),
                                   FigDims[0].astype(int)))
        mpl.rc('image', cmap='gray')

    return f



