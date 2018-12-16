from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from statistics import mean
from AnalyseScripts.Analyse import *
import numpy as np
import scipy as sp


class LoopWorker(QObject):
    results = pyqtSignal(int, np.ndarray)
    errors = pyqtSignal(int, str)
    final = pyqtSignal(int)
    progress = pyqtSignal(str)
    current_results = pyqtSignal(bool, float, float, float, np.ndarray) # err ok, mean, rate, volts, curr_array

    def __init__(self, meter, *args, **kwargs):
        super().__init__()# very new way to call super() method.
        self.args = args
        self.params = kwargs
        self.meter = meter
        self._require_stop = False
        self._measurement_parameters = {}
        self.curr = None
        self.volt = None
        self.err_ok=False
        # Few globals
        self.current_scale=None
        pass

    @pyqtSlot()
    def run(self):
        try:
            # current_scale=None
            counter=0
            startV = self.params['startV']
            endV = self.params['endV']
            array_size = self.params['array_size']
            step = (endV - startV)/self.params['points']
            totalV = startV
            limit = self.params['x_mean']
            self.prepare_source_meter(array_size)
            fb_scan = self.params['fb_scan']
            print("(y)")
            print(fb_scan)
            #self.curr_array.append(totalV) # what the hell is this?
            if 0 == fb_scan:
                while (totalV >= endV):
                    while not self.err_ok:
                        curr_array = self.sample_measurement(totalV)
                        status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit, self.current_scale)
                        if overflow:
                            curr_range = self.meter.getCurrentSensorRange()
                            new_scale = getBiggerScale(curr_range)
                            self.meter.setCurrentSensorRange(new_scale)
                            self.current_scale = new_scale
                            status = False
                            pass
                        if underflow:
                            new_scale = getLowerScale(self.current_scale)
                            self.meter.setCurrentSensorRange(new_scale)
                            self.current_scale = new_scale
                            status=False
                        counter=counter+1
                        if counter>15 and not overflow:
                            status=True
                        self.current_results.emit(status, data_mean, err_rate, totalV, curr_array)
                        self.err_ok = status
                        pass
                    # print('++++++++++++++++++++++++++++')
                    # self.meter.setMeasurementRange(0.03)
                    time.sleep(1)
                    totalV = totalV + step
                    self.err_ok = False
                    # print('totalV', totalV)
                    # print('step', step)
                self.stop_measurement()
            #     TODO this part is incomplete!
            elif fb_scan == 1:
                while (totalV >= endV):
                    while not self.err_ok:
                        curr_array = self.sample_measurement(totalV)
                        status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit, self.current_scale)
                        if overflow:
                            curr_range = self.meter.getCurrentSensorRange()
                            new_scale = getBiggerScale(curr_range)
                            self.meter.setCurrentSensorRange(new_scale)
                            self.current_scale = new_scale
                            status = False
                            pass
                        if underflow:
                            new_scale = getLowerScale(self.current_scale)
                            self.meter.setCurrentSensorRange(new_scale)
                            self.current_scale = new_scale
                            status=False
                        counter=counter+1
                        if counter>15 and not overflow:
                            status=True
                        self.current_results.emit(status, data_mean, err_rate, totalV, curr_array)
                        self.err_ok = status
                        pass
                    # print('++++++++++++++++++++++++++++')
                    # self.meter.setMeasurementRange(0.03)
                    time.sleep(1)
                    totalV = totalV + step
                    self.err_ok = False
                    # print('totalV', totalV)
                    # print('step', step)
                # self.stop_measurement()
                #Second while loop
                while (totalV <= endV):
                    while not self.err_ok:
                        curr_array = self.sample_measurement(totalV)
                        status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit, self.current_scale)
                        if overflow:
                            curr_range = self.meter.getCurrentSensorRange()
                            new_scale = getBiggerScale(curr_range)
                            self.meter.setCurrentSensorRange(new_scale)
                            self.current_scale = new_scale
                            status = False
                            pass
                        if underflow:
                            new_scale = getLowerScale(self.current_scale)
                            self.meter.setCurrentSensorRange(new_scale)
                            self.current_scale = new_scale
                            status=False
                        counter=counter+1
                        if counter>15 and not overflow:
                            status=True
                        self.current_results.emit(status, data_mean, err_rate, totalV, curr_array)
                        self.err_ok = status
                        pass
                    # print('++++++++++++++++++++++++++++')
                    # self.meter.setMeasurementRange(0.03)
                    time.sleep(1)
                    totalV = totalV - step
                    self.err_ok = False
                    # print('totalV', totalV)
                    # print('step', step)
                self.stop_measurement()
            else:
                print("ERR.CODE.SHIT")
                print(str(fb_scan))
        except Exception as ex:
            print("ERR.CODE.001")
            print(str(ex))
        pass


    def prepare_source_meter(self, array_size):
        """
        We need to do this just once, before all measurements

        :param array_size:
        :return:
        """
        try:
            self.meter.setMeasurementRange(2e-4) # 200 μA range?
            self.current_scale=2e-4 #
            # self.meter.setCurrentAutoRangeLLIM(2e-9) # 2 nA lower limit
            # self.meter.setCurrentAutoRangeULIM(1e-6) # 1 μA upper limit
            self.meter.setMeasurementSpeed(10) # 10 NPLC
            self.meter.setTriggerDelay()  # no parameter is used for zero delay
            self.meter.setTriggerSource(self.meter.TRIGGER_TIM)
            self.meter.setTriggerTimerInterval(0.004) # hardcoded?
            self.meter.setTriggerCounts(array_size)
        except Exception as ex:
            print("ERR.CODE.002")
            print(str(ex))
        pass


    def sample_measurement(self, voltage):
        data_np = None
        try:
            self.meter.setVoltOutValue(voltage)
            self.meter.enableVoltageOutput(self.meter.bON)
            self.meter.enableAmmeterInput(self.meter.bON)
            self.meter.initAcquire()
            # Give enough time for this action
            time.sleep(1) # one second is enough?
            data = self.meter.fetchArrayData(self.meter.CURR) #
            data_np = np.fromstring(data, dtype=float, sep=",")
        except Exception as ex:
            print("ERR.CODE.003")
            print(str(ex))
        return data_np

    def stop_measurement(self):
        try:
            self.meter.enableAmmeterInput(self.meter.bOFF)
            self.meter.enableVoltageOutput(self.meter.bOFF)
        except Exception as ex:
            print("ERR.CODE.004")
            print(str(ex))
        pass