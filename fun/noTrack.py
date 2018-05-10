# -*- coding: utf-8 -*-
"""
Adam Tyson | adam.tyson@icr.ac.uk | 2018-05-10

@author: Adam Tyson
"""

import os
import tools.detection as dt


def noTrackRun(var):
    allFiles = os.listdir('.')
    for file in allFiles:
        objCent = dt.obj_cent(file, var.plot)
        cellsF = dt.cell_detect(file, var)
        celldf = dt.cellDist(cellsF, objCent, var.plot)