import numpy as np
import scipy as sp
import math


def getErrorsRate(_np_array):
    min = np.amin(_np_array)
    max=np.amax(_np_array)
    mean = np.mean(_np_array)
    return (max-min)/mean, mean
    pass

def convertToNpArray(_array):
    return np.asarray(_array)

def getStats(_array, limit):
    limit_stat = True
    _np_array = convertToNpArray(_array)
    rate, mean = getErrorsRate(_np_array)
    if rate>limit:
        limit_stat = False
    elif rate <= limit:
        limit_stat = True
    else:
        limit_stat=True
    return limit_stat, mean, rate
    pass