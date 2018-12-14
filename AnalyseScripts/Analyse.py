import numpy as np
import scipy as sp
import math


def getErrorsRate(_np_array):
    overflow= False
    min = np.amin(_np_array)
    max=np.amax(_np_array)
    if (max >= 1e2):
        overflow = True
    mean = np.mean(_np_array)
    return (max-min)/mean, mean, overflow
    pass


def getStats(_array, limit):
    limit_stat = True
    #_np_array = convertToNpArray(_array)
    rate, mean, overflow = getErrorsRate(_array)
    if rate>limit:
        limit_stat = False
    elif rate <= limit:
        limit_stat = True
    else:
        limit_stat=True
    return limit_stat, mean, rate, overflow
    pass


def getBiggerScale(curr_scale):
    c_scale = float(curr_scale)
    new_scale = c_scale * 10
    return new_scale
    pass