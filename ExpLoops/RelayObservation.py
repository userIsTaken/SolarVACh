from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from statistics import mean
from AnalyseScripts.Analyse import *
import numpy as np
import scipy as sp


class RelayObserver(QObject):
    def __init__(self):
        super(RelayObserver, self).__init__()
        pass