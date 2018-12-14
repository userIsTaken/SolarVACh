import numpy as np
import scipy as sp
import math


def getErrorsRate(_np_array, current_scale):
    overflow= False
    underflow=False
    min = np.amin(_np_array)
    max=np.amax(_np_array)
    if (max <= -1e2):
        overflow = True
    if (max >= 1e2):
        overflow = True
    mean = np.mean(_np_array)
    if abs(mean) < 0.05*current_scale:
        underflow = True
    return (max-min)/mean, mean, overflow, underflow
    pass


def getStats(_array, limit, current_scale):
    limit_stat = True
    #_np_array = convertToNpArray(_array)
    rate, mean, overflow, underflow = getErrorsRate(_array, current_scale)
    if rate>limit:
        limit_stat = False
    elif rate <= limit:
        limit_stat = True
    else:
        limit_stat=True
    return limit_stat, mean, rate, overflow, underflow
    pass


def getBiggerScale(curr_scale):
    c_scale = float(curr_scale)
    new_scale = c_scale * 10.0
    return new_scale
    pass

def getLowerScale(curr_scale):
    c_scale = float(curr_scale)
    new_scale = c_scale / 10.0
    return new_scale
    pass