import numpy as np
import scipy as sp
import math


def getErrorsRate(_np_array):
    min = np.amin(_np_array)
    max=np.amax(_np_array)
    mean = np.mean(_np_array)
    return (max-min)/mean, mean
    pass


def getStats(_array, limit):
    limit_stat = True
    scale_change=False
    #_np_array = convertToNpArray(_array)
    rate, mean = getErrorsRate(_array)
    if rate>limit:
        limit_stat = False
    elif rate <= limit:
        limit_stat = True
    else:
        limit_stat=True
    if mean < 1e-6:
        scale_change = True
    else:
        scale_change = False
    return limit_stat, mean, rate, scale_change
    pass


# def getScaleChange(current_scale, mean):
#     change, new_scale = False, None
#     if str(current_scale).lower() in 'auto':
#         if mean < 1e-6:
#             change = True
#             new_scale = 1e-6
#     else:
#         if mean < current_scale:
#             pass
#
#     return change, new_scale
#     pass