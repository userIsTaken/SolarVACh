from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from statistics import mean
from AnalyseScripts.Analyse import *
import numpy as np
import scipy as sp


class LoopWorker(QObject):
    # TODO: delete all unnecessary signals:
    # results = pyqtSignal(int, np.ndarray)
    errors = pyqtSignal(int, str)
    final = pyqtSignal(bool)
    progress = pyqtSignal(str)
    trigger = pyqtSignal(bool, bool) # trigger and fb_scan value ( 0 - False, 2 - True)
    relay = pyqtSignal(int)
    current_results = pyqtSignal(bool, bool, float, float, float, np.ndarray) # err ok, fb_scan, mean, rate, volts, curr_array

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
        self.current_array_counter=[] # empty list
        pass

    @pyqtSlot()
    def run(self):
        # TODO : We need to implement relay control here also
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
            self._require_stop = False
            # print("(y)")
            # print(fb_scan)
            #self.curr_array.append(totalV) # what the hell is this?
            if 0 == fb_scan:
                while (totalV >= endV and not self._require_stop):
                    while not self.err_ok and not self._require_stop:
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
                        # print('counter', counter)
                        self.progress.emit("Counter: "+str(counter))
                        if not status and not overflow:
                            self.current_array_counter.append(data_mean)
                        else:
                            self.current_array_counter.clear()
                        if counter>15 and not overflow:
                            status=True
                            data_mean = np.mean(np.asarray(self.current_array_counter))
                            # print("counter is 16, ", data_mean)
                            self.progress.emit("Counter : 16, "+str(data_mean))
                            self.current_array_counter.clear()
                        self.current_results.emit(status, False, data_mean, err_rate, totalV, curr_array)
                        self.err_ok = status
                        pass
                    # print('++++++++++++++++++++++++++++')
                    # self.meter.setMeasurementRange(0.03)
                    time.sleep(1)
                    counter = 0
                    totalV = totalV + step
                    self.err_ok = False
                    # print('totalV', totalV)
                    # print('step', step)
                self.trigger.emit(True, False)
                self.stop_measurement()
            #     TODO this part is incomplete!
            #     TODO: This part needs to be checked again, seems to be working
            elif fb_scan == 2:
                while (totalV >= endV and not self._require_stop):
                    while not self.err_ok and not self._require_stop:
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
                        # print('counter', counter)
                        self.progress.emit("Counter: " + str(counter))
                        if not status and not overflow:
                            self.current_array_counter.append(data_mean)
                        else:
                            self.current_array_counter.clear()
                        if counter>15 and not overflow:
                            status=True
                            data_mean = np.mean(np.asarray(self.current_array_counter))
                            # print("counter is 16, ", data_mean)
                            self.progress.emit("Counter : 16, " + str(data_mean))
                            self.current_array_counter.clear()
                        self.current_results.emit(status, False, data_mean, err_rate, totalV, curr_array)
                        self.err_ok = status
                        pass
                    # print('++++++++++++++++++++++++++++')
                    # self.meter.setMeasurementRange(0.03)
                    time.sleep(1)
                    counter = 0
                    totalV = totalV + step
                    self.err_ok = False
                    # print('totalV', totalV)
                    # print('step', step)
                self.trigger.emit(True, False)
                #     second loop:
                while (totalV <= startV and not self._require_stop):
                    while not self.err_ok and not self._require_stop:
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
                        # print('counter', counter)
                        self.progress.emit("Counter: " + str(counter))
                        if not status and not overflow:
                            self.current_array_counter.append(data_mean)
                        else:
                            self.current_array_counter.clear()
                        if counter>15 and not overflow:
                            status=True
                            data_mean = np.mean(np.asarray(self.current_array_counter))
                            # print("counter is 16, ", data_mean)
                            self.progress.emit("Counter : 16, " + str(data_mean))
                            self.current_array_counter.clear()
                        self.current_results.emit(status, True, data_mean, err_rate, totalV, curr_array)
                        self.err_ok = status
                        pass
                    # print('++++++++++++++++++++++++++++')
                    # self.meter.setMeasurementRange(0.03)
                    time.sleep(1)
                    counter = 0
                    totalV = totalV - step
                    self.err_ok = False
                    # print('totalV', totalV)
                    # print('step', step)
                self.trigger.emit(True, True)
                self.stop_measurement()
            else:
                print("ERR.CODE.SHIT")
                print(str(fb_scan), " FB SCAN VALUE")
                self.errors.emit(1, "ERR.CODE.SHIT\n"+str(fb_scan)+" FB SCAN VALUE")
        except Exception as ex:
            print("ERR.CODE.001")
            print(str(ex))
            self.errors.emit(1, "ERR.CODE.001"+str(ex))
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

    # @pyqtSlot()
    def stop_measurement(self):
        try:
            self.meter.enableAmmeterInput(self.meter.bOFF)
            self.meter.enableVoltageOutput(self.meter.bOFF)
            self.final.emit(True)
        except Exception as ex:
            print("ERR.CODE.004")
            print(str(ex))
            print("ERROR IN: stop_measurement function")
        pass

    @pyqtSlot()
    def stop(self):
        self._require_stop = True
        self.stop_measurement()
        pass