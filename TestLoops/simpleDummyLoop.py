from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from HardwareAccess.KeysightWrapper import SourceMeter
import sys
import numpy


class dummyLoop(QObject):
    results = pyqtSignal(list, list, list, str, dict)
    errors = pyqtSignal(int, str)
    final = pyqtSignal(int)
    progress = pyqtSignal(str)
    def __init__(self, sourcemeter, parameters, *args, **kwargs):
        super(dummyLoop, self).__init__()
        self.sMeter=sourcemeter
        self.parameters = parameters
        pass

    @pyqtSlot()
    def startMeasurement(self):
        startVoltage = self.parameters['startV']
        stopVoltage = self.parameters['stopV']

        pass
