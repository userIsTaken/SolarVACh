import numpy as np
import scipy as sp
import math


def getErrorsRate(_np_array):
    min = np.amin(_np_array)
    max=np.amax(_np_array)
    if (max >= 1e6):
        pass
    mean = np.mean(_np_array)
    return (max-min)/mean, mean
    pass


def getStats(_array, limit):
    limit_stat = True
    #_np_array = convertToNpArray(_array)
    rate, mean = getErrorsRate(_array)
    if rate>limit:
        limit_stat = False
    elif rate <= limit:
        limit_stat = True
    else:
        limit_stat=True
    return limit_stat, mean, rate
    pass


def getScaleChange(mean):
    new_scale=0.03
    if mean < 1e-9:
        new_scale = 2e-9
    elif mean < 1e-8:
        new_scale = 2e-8
    elif mean < 1e-7:
        new_scale = 2e-7
    elif mean < 1e-6:
        new_scale = 2e-6
    return new_scale
    pass