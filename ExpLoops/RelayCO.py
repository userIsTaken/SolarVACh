from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from statistics import mean
from AnalyseScripts.Analyse import *
import numpy as np
import scipy as sp
from HardwareAccess.gpio_relays import *
import traceback


class RelayCO(QObject):
    # results = pyqtSignal(int, np.ndarray)
    errors = pyqtSignal(int, str)
    final = pyqtSignal(bool)
    progress = pyqtSignal(str)
    trigger = pyqtSignal(bool, bool, float, str, int)  # trigger and fb_scan value ( 0 - False, 2 - True)
    #relay = pyqtSignal(int)
    current_results = pyqtSignal(bool, bool, float, float, float,
                                 np.ndarray, str, bool, int)  # err ok, fb_scan, mean, rate, volts, curr_array

    def __init__(self, meter, *args, **kwargs):
        super().__init__()  # very new way to call super() method.
        self.args = args
        self.params = kwargs
        self.meter = meter
        self._require_stop = False
        self._measurement_parameters = {}
        self.curr = None
        self.volt = None
        self.err_ok = False
        # Few globals
        self.current_scale = None
        self.current_array_counter = []  # empty list
        self.time_delay = self.params['delay_min']*60 # delay in seconds
        self.counts = self.params['counts']
        self.relay = None
        pass

    @pyqtSlot()
    def run(self):
        # TODO : observation over time
        try:
            # current_scale=None
            observation_counter = 0
            counter = 0
            startV = self.params['startV']
            endV = self.params['endV']
            array_size = self.params['array_size']
            step = (endV - startV) / self.params['points']
            totalV = startV
            limit = self.params['x_mean']
            self.prepare_source_meter(array_size)
            fb_scan = self.params['fb_scan']
            self._require_stop = False
            rel = self.params['relay_combo'] + 1
            first_rel = self.params['relay_combo'] + 1
            elec = self.params['el_combo'] + 1
            name = '1 el.'
            elec_nr = 1
            color = 1
            # print("(y)")
            # print(fb_scan)
            # self.curr_array.append(totalV) # what the hell is this?
            # ========================================================
            #  START of a counter:
            # ========================================================
            while (observation_counter <= self.counts and not self._require_stop):
                # ========================================================
                #  START of a measurement loop:
                # ========================================================
                while (rel < first_rel + elec):
                    self.relay = RelayToggle(str(rel))
                    self.relay.toggle(self.relay.ON)
                    name = '_' + str(elec_nr) + 'el.'
                    # print("(y)")
                    # print(fb_scan)
                    # self.curr_array.append(totalV) # what the hell is this?
                    if 0 == fb_scan:
                        while (totalV > (endV + step) and not self._require_stop):
                            while not self.err_ok and not self._require_stop:
                                curr_array = self.sample_measurement(totalV)
                                status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit,
                                                                                            self.current_scale)
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
                                    status = False
                                counter = counter + 1
                                # print('counter', counter)
                                self.progress.emit("Counter: " + str(counter))
                                if not status and not overflow:
                                    self.current_array_counter.append(data_mean)
                                else:
                                    self.current_array_counter.clear()
                                if counter > 15 and not overflow:
                                    status = True
                                    data_mean = np.mean(np.asarray(self.current_array_counter))
                                    # print("counter is 16, ", data_mean)
                                    self.progress.emit("Counter : 16, " + str(round(data_mean, 4)))
                                    self.current_array_counter.clear()
                                self.current_results.emit(status, False, data_mean, err_rate, totalV, curr_array, name,
                                                          False, color)
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
                        if not self._require_stop:
                            self.trigger.emit(True, False, observation_counter, name, color)
                        self.stop_measurement()
                    #     TODO this part is incomplete!
                    #     TODO: This part needs to be checked again, seems to be working
                    elif fb_scan == 2:
                        while (totalV > (endV + step) and not self._require_stop):
                            while not self.err_ok and not self._require_stop:
                                curr_array = self.sample_measurement(totalV)
                                status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit,
                                                                                            self.current_scale)
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
                                    status = False
                                counter = counter + 1
                                # print('counter', counter)
                                self.progress.emit("Counter: " + str(counter))
                                if not status and not overflow:
                                    self.current_array_counter.append(data_mean)
                                else:
                                    self.current_array_counter.clear()
                                if counter > 15 and not overflow:
                                    status = True
                                    data_mean = np.mean(np.asarray(self.current_array_counter))
                                    # print("counter is 16, ", data_mean)
                                    self.progress.emit("Counter : 16, " + str(round(data_mean, 4)))
                                    self.current_array_counter.clear()
                                self.current_results.emit(status, False, data_mean, err_rate, totalV, curr_array, name,
                                                          False, color)
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
                        if not self._require_stop:
                            self.trigger.emit(True, False, observation_counter, name, color)
                        #     second loop:
                        totalV = endV
                        while (totalV <= (startV - step) and not self._require_stop):  # +/- step?
                            while not self.err_ok and not self._require_stop:
                                curr_array = self.sample_measurement(totalV)
                                status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit,
                                                                                            self.current_scale)
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
                                    status = False
                                counter = counter + 1
                                # print('counter', counter)
                                self.progress.emit("Counter: " + str(counter))
                                if not status and not overflow:
                                    self.current_array_counter.append(data_mean)
                                else:
                                    self.current_array_counter.clear()
                                if counter > 15 and not overflow:
                                    status = True
                                    data_mean = np.mean(np.asarray(self.current_array_counter))
                                    # print("counter is 16, ", data_mean)
                                    self.progress.emit("Counter : 16, " + str(round(data_mean, 4)))
                                    self.current_array_counter.clear()
                                self.current_results.emit(status, True, data_mean, err_rate, totalV, curr_array, name,
                                                          False, color)
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
                        if not self._require_stop:
                            self.trigger.emit(True, True, observation_counter, name, color)
                        self.stop_measurement()
                    else:
                        # tcbk.print_exc()
                        print("ERR.CODE.SHIT")
                        print(str(fb_scan), " FB SCAN VALUE")
                        self.errors.emit(1, "ERR.CODE.SHIT\n" + str(fb_scan) + " FB SCAN VALUE")
                    self.relay.toggle(self.relay.OFF)
                    rel = rel + 1
                    elec_nr = elec_nr + 1
                    startV = self.params['startV']
                    endV = self.params['endV']
                    totalV = startV
                    self.current_results.emit(status, False, data_mean, err_rate, totalV, curr_array, name, True, color)
                    time.sleep(1)
                    color = color + 1
                #===========================================================
                # END of a measurement loop
                #===========================================================
                # Return initial values
                startV = self.params['startV']
                endV = self.params['endV']
                totalV = startV
                # sleep
                time.sleep(self.time_delay)
                # change counter
                observation_counter = observation_counter + 1
                rel = self.params['relay_combo'] + 1
                elec = self.params['el_combo'] + 1
                color = 1
                elec_nr = 1
            #===========================================================
            # END of counter
            self.final.emit(True)
            #===========================================================
        except Exception as ex:
            print("ERR.CODE.001")
            print(str(ex))
            self.errors.emit(1, "ERR.CODE.001" + str(ex))
        pass

    def prepare_source_meter(self, array_size):
        """
        We need to do this just once, before all measurements

        :param array_size:
        :return:
        """
        try:
            trig_time_int = self.params['wait']/1000 # convert into seconds
            self.meter.setMeasurementRange(2e-4) # 200 μA range?
            self.current_scale=2e-4 #
            # self.meter.setCurrentAutoRangeLLIM(2e-9) # 2 nA lower limit
            # self.meter.setCurrentAutoRangeULIM(1e-6) # 1 μA upper limit
            self.meter.setMeasurementSpeed(self.params['nplc']) # 0.1 NPLC
            self.meter.setTriggerDelay()  # no parameter is used for zero delay
            self.meter.setTriggerSource(self.meter.TRIGGER_TIM)
            self.meter.setTriggerTimerInterval(trig_time_int) # hardcoded?
            self.meter.setTriggerCounts(array_size)
        except Exception as ex:
            traceback.print_exc()
            print("ERR.CODE.002")
            print(str(ex))
        pass

    def sample_measurement(self, voltage):
        data_np = None
        try:
            self.meter.setVoltOutValue(voltage)
            # print("Voltage")
            # time.sleep(20)
            self.meter.enableVoltageOutput(self.meter.bON)
            # print('output on')
            # time.sleep(20)
            self.meter.enableAmmeterInput(self.meter.bON)
            # time.sleep(20)
            self.meter.initAcquire()
            # print('init aquire')
            # time.sleep(20)
            # Give enough time for this action
            time.sleep(1)  # one second is enough?
            data = self.meter.fetchArrayData(self.meter.CURR)  #
            # print('data')
            # time.sleep(20)
            if data is not None:
                data_np = np.fromstring(data, dtype=float, sep=",")
            self.meter.clearBuffer()
            # print('buffer clear')
        except Exception as ex:
            traceback.print_exc()
            print("ERR.CODE.003")
            print(str(ex))
        return data_np

    # @pyqtSlot()
    def stop_measurement(self):
        try:
            self.meter.enableAmmeterInput(self.meter.bOFF)
            self.meter.enableVoltageOutput(self.meter.bOFF)
            self.meter.setVoltOutValue(0)
            # self.final.emit(True)
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