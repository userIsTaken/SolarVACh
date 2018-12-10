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
        #self.curr_array = []
        #self.volt_array = []
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
            self.prepare_source_meter(array_size)
            #self.curr_array.append(totalV) # what the hell is this?
            while (totalV <= endV):
                while not self.err_ok:
                    curr_array = self.sample_measurement(totalV)
                    status, data_mean, err_rate = getStats(curr_array)
                    self.current_results.emit(status, data_mean, err_rate, totalV, curr_array)
                    self.err_ok = status
                    pass
                totalV = totalV + step
            self.stop_measurement()
        except Exception as ex:
            print(str(ex))
        pass


    def prepare_source_meter(self, array_size):
        """
        We need to do this once, before all measurements

        :param array_size:
        :return:
        """
        self.meter.setMeasurementRange("auto")
        self.meter.setMeasurementSpeed()
        self.meter.setTriggerDelay()  # no parameter is used for zero delay
        self.meter.setTriggerSource(self.meter.TRIGGER_TIM)
        self.meter.setTriggerTimerInterval(0.004) # hardcoded?
        self.meter.setTriggerCounts(array_size)
        pass


    def sample_measurement(self, voltage):
        self.meter.setVoltOutValue(voltage)
        self.meter.enableVoltageOutput(self.meter.bON)
        self.meter.enableAmmeterInput(self.meter.bON)
        self.meter.initAcquire()
        # Give enough time for this action
        time.sleep(1) # one second is enough?
        data = self.meter.fetchArrayData(self.meter.CURR) #
        data_np = np.fromstring(data, dtype=float, sep=",")
        return data_np
        pass

    def stop_measurement(self):
        self.meter.enableAmmeterInput(self.meter.bOFF)
        self.meter.enableVoltageOutput(self.meter.bOFF)

        pass