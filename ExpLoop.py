from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time


class LoopWorker(QObject):
    results = pyqtSignal()
    errors = pyqtSignal(int, str)
    final = pyqtSignal(int)
    progress = pyqtSignal(str)

    def __init__(self, meter, *args, **kwargs):
        super(LoopWorker, self).__init__()
        self.args = args
        self.params = kwargs
        self.meter = meter
        self._require_stop = False
        self._measurement_parameters = {}
        pass

    @pyqtSlot()
    def run(self):
        try:
            startV = self.params['startV']
            endV = self.params['endV']
            self.results.emit()
        except:
            print('blah')
        pass


    def sample_measure(self, array_size):
        self.meter.setMeasurementRange(2e-9)
        self.meter.setMeasurementSpeed()
        #self.meter.adjustTrigTiming() not implemented
        #’ Adjust trigger timing parameters
        #ioObj.WriteString(":trig:acq:del 2.0e-3")   (from Keysight example)
        #needed??????
        self.meter.setTriggerSource(1)
        self.meter.setTriggerTimerInterval(0.004)
        self.meter.setTriggerCounts(array_size)
        self.meter.enableAmmeterInput(True)
        self.meter.initAcquire()
        data = self.meter.fetchArrayData("CURRENT") #not sure if it's the right way to address [if (_atype.capitalize() in "CURRENT" ):]
        return data
        pass
