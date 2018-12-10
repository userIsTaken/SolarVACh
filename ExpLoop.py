from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from statistics import mean
from AnalyseScripts.Analyse import *
import numpy as np
import scipy as sp


class LoopWorker(QObject):
    results = pyqtSignal(list, list)
    errors = pyqtSignal(int, str)
    final = pyqtSignal(int)
    progress = pyqtSignal(str)
    current_results = pyqtSignal(bool, float, float, float, list) # err ok, mean, rate, volts, curr_array

    def __init__(self, meter, *args, **kwargs):
        super(LoopWorker, self).__init__()
        self.args = args
        self.params = kwargs
        self.meter = meter
        # self.data = None
        self.curr_array = []
        self.volt_array = []
        self._require_stop = False
        self._measurement_parameters = {}
        self.curr = None
        self.volt = None
        self.err_ok=False
        # self.data_np=None
        pass

    @pyqtSlot()
    def run(self):
        try:
            startV = self.params['startV']
            endV = self.params['endV']
            array_size = self.params['array_size']
            step = (endV - startV)/self.params['points']
            totalV = startV
            self.curr_array.append(totalV)
            while (totalV <= endV):
                while not self.err_ok:
                    self.curr_array = self.sample_measurement(array_size)
                    status, data_mean, err_rate = getStats(self.curr_array)
                    self.current_results.emit(self.err_ok, data_mean, err_rate,totalV, self.curr_array)
                    self.err_ok = status
                    pass
                # self.curr_array.append(mean(self.sample_measurement(array_size)))
                # self.results.emit(self.volt_array, self.curr_array)# re-think it
                totalV = totalV + step
                # self.volt_array.append(totalV)
            self.stop_measurement()
        except:
            print('blah')
        pass


    def sample_measurement(self, array_size, voltage):
        self.meter.setMeasurementRange(2e-9)
        self.meter.setMeasurementSpeed()
        #self.meter.adjustTrigTiming() not implemented
        #’ Adjust trigger timing parameters
        #ioObj.WriteString(":trig:acq:del 2.0e-3")   (from Keysight example)
        #needed?????? Nope, delay has to be equal to zero.
        self.meter.setTriggerDelay() # no parameter is used for zero delay
        self.meter.setTriggerSource(self.meter.TRIGGER_TIM)
        self.meter.setTriggerTimerInterval(0.004)
        self.meter.setTriggerCounts(array_size)
        self.meter.setVoltOutValue(voltage)
        self.meter.enableVoltageOutput(self.meter.bON)
        self.meter.enableAmmeterInput(self.meter.bON)
        self.meter.initAcquire()
        data = self.meter.fetchArrayData(self.meter.CURR) #
        data_np = np.fromstring(data, dtype=float, sep=",")
        return data_np
        pass
    def stop_measurement(self):
        self.meter.enableAmmeterInput(self.meter.bOFF)
        self.meter.enableVoltageOutput(self.meter.bOFF)

        pass