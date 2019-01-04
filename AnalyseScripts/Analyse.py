import numpy as np
import scipy as sp
import math


def getErrorsRate(_np_array, current_scale):
    """

    :param _np_array:
    :param current_scale:
    :return:
    """
    overflow= False
    underflow=False
    min = np.amin(_np_array)
    max=np.amax(_np_array)
    if (min <= -1e2):
        overflow = True
    if (max >= 1e2):
        overflow = True
    mean = np.mean(_np_array)
    x = mean
    # print('---------------')
    # print('mean', mean)
    # print('current_scale', current_scale)
    # print('---------------')
    if abs(mean) < 0.05*current_scale and abs(mean) < 1e2 and abs(mean) > 0.0:
        underflow = True
    if mean == 0.0:
        x = 1.0
    return abs(abs(max)-abs(min))/abs(x), mean, overflow, underflow
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

def getClosestValue(array, value):
    """
    Returns the closest value to an argument

    :param value: value to compare
    :param array: array to inspect
    :return:
    """
    array = np.asarray(array)
    # idx = None
    # try:
    #     idx = (np.abs(array - value)).argmin()
    # except Exception as ex:
    #     print(str(ex))
    #     idx = 0
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def closestValueIndex(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def getPCE(pmax, solarP):
    """

    :param pmax:
    :param solarP:
    :return:
    """
    pce = abs(pmax)/solarP * 100.0 # in percents
    return pce
    pass

def getMaxPJV(current, voltage):
    """

    :param current:
    :param voltage:
    :return: p_max, curr_max, volt_max => W, A, V !
    """
    P = np.asarray([a * b for a,b in zip(current, voltage)])
    p_idx = P.argmin()
    p_max = P.min()
    curr_max = current[p_idx]
    volt_max = voltage[p_idx]
    return p_max, curr_max, volt_max
    pass

def getFF(maxp, uoc, jsc):
    """

    :param maxp:
    :param uoc:
    :param jsc:
    :return:
    """
    ff = maxp/(uoc*jsc) * 100 # in %
    return ff
    pass