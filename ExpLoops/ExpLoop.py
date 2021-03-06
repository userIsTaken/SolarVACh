from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time
# from statistics import mean
from AnalyseScripts.Analyse import *
import numpy as np
import scipy as sp
import traceback
from HardwareAccess.MotorWrapper import *
from Config.confparser import getGPIOip
from HardwareAccess.gpio_relays import *

from vars import *


class LoopWorker(QObject):
    # TODO: delete all unnecessary signals:
    # results = pyqtSignal(int, np.ndarray)
    errors = pyqtSignal(int, str)
    final = pyqtSignal(bool)
    progress = pyqtSignal(str)
    trigger = pyqtSignal(bool, bool, float, str) # trigger and fb_scan value ( 0 - False, 2 - True), counter for time observer, name(dark light)
    #relay = pyqtSignal(int)
    current_results = pyqtSignal(bool, bool, float, float, float, np.ndarray, str) # err ok, fb_scan, mean, rate, volts, curr_array

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
        self.name = None
        self.relay = None
        pass



    @pyqtSlot()
    def run(self):
        try:
            # current_scale=None
            motor = Motor()
            motor.set_ip(getGPIOip())
            motor.setup()
            counter=0
            startV = self.params['startV']
            endV = self.params['endV']
            array_size = self.params['array_size']
            step = (endV - startV)/self.params['points']
            totalV = startV
            limit = self.params['x_mean']
            self.prepare_source_meter(array_size)
            fb_scan = self.params['fb_scan']
            dark = self.params['dark_scan'] # 0 or 2 (unchecked or checked)
            self._require_stop = False
            name = ''
            if self.params['cRel']:
                console("VAL of cRel", self.params['cRel'])
                rel = self.params['relay_combo']+1
                self.relay = RelayToggle(str(rel))
                self.relay.toggle(self.relay.ON)
            while dark >= 0:
                if dark == 2:
                    motor.move_motor_cw()
                    motor.Status = True
                    name = 'dark'
                    self.name = name
                elif dark == 0 and motor.Status:
                    motor.move_motor_ccw()
                    motor.Status = False
                    name = 'light'
                    self.name = name
                # MAIN LOOP with all measurements:
                if 0 == fb_scan:
                    while (totalV > (endV+step) and not self._require_stop):
                        while not self.err_ok and not self._require_stop:
                            curr_array = self.sample_measurement(totalV)
                            if curr_array is not None:
                                status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit, self.current_scale)
                                if overflow:
                                    curr_range = self.meter.getCurrentSensorRange()
                                    new_scale = getBiggerScale(curr_range)
                                    if new_scale is not None and new_scale >= 0.021:
                                        self.stop_now()
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
                                    self.progress.emit("Counter : 16, "+str(round(data_mean, 4)))
                                    self.current_array_counter.clear()
                                self.current_results.emit(status, False, data_mean, err_rate, totalV, curr_array, name)
                                self.err_ok = status
                                pass
                            else:
                                self.errors.emit("data is None from source meter")
                                self._require_stop = True
                        # print('++++++++++++++++++++++++++++')
                        # self.meter.setMeasurementRange(0.03)
                        time.sleep(1)
                        counter = 0
                        totalV = totalV + step
                        self.err_ok = False
                        # print('totalV', totalV)
                        # print('step', step)
                    if not self._require_stop:
                        self.trigger.emit(True, False, -1, self.name)
                    self.stop_measurement()
                #     TODO this part is incomplete!
                #     TODO: This part needs to be checked again, seems to be working
                elif fb_scan == 2:
                    while (totalV > (endV+step) and not self._require_stop):
                        while not self.err_ok and not self._require_stop:
                            curr_array = self.sample_measurement(totalV)
                            if curr_array is not None:
                                # pass
                                status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit, self.current_scale)
                                if overflow:
                                    curr_range = self.meter.getCurrentSensorRange()
                                    new_scale = getBiggerScale(curr_range)
                                    if new_scale is not None and new_scale >= 0.021:
                                        self.stop_now()
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
                                    self.progress.emit("Counter : 16, " + str(round(data_mean, 4)))
                                    self.current_array_counter.clear()
                                self.current_results.emit(status, False, data_mean, err_rate, totalV, curr_array, name)
                                self.err_ok = status
                                pass
                            else:
                                self.errors.emit("data is None from source meter")
                                self._require_stop = True
                        # print('++++++++++++++++++++++++++++')
                        # self.meter.setMeasurementRange(0.03)
                        time.sleep(1)
                        counter = 0
                        totalV = totalV + step
                        self.err_ok = False
                        # print('totalV', totalV)
                        # print('step', step)
                    if not self._require_stop:
                        self.trigger.emit(True, False, -1, self.name)
                    #     second loop:
                    totalV = endV
                    while (totalV <= (startV-step) and not self._require_stop): #+/- step?
                        while not self.err_ok and not self._require_stop:
                            curr_array = self.sample_measurement(totalV)
                            if curr_array is not None:
                                status, data_mean, err_rate, overflow, underflow = getStats(curr_array, limit, self.current_scale)
                                if overflow:
                                    curr_range = self.meter.getCurrentSensorRange()
                                    new_scale = getBiggerScale(curr_range)
                                    if new_scale is not None and new_scale >= 0.021:
                                        self.stop_now()
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
                                    self.progress.emit("Counter : 16, " + str(round(data_mean, 4)))
                                    self.current_array_counter.clear()
                                self.current_results.emit(status, True, data_mean, err_rate, totalV, curr_array, name)
                                self.err_ok = status
                                pass
                            else:
                                self.errors.emit("data is None from source meter")
                                self._require_stop = True
                        # print('++++++++++++++++++++++++++++')
                        # self.meter.setMeasurementRange(0.03)
                        time.sleep(1)
                        counter = 0
                        totalV = totalV - step
                        self.err_ok = False
                        # print('totalV', totalV)
                        # print('step', step)
                    if not self._require_stop:
                        self.trigger.emit(True, True, -1, self.name)
                    self.stop_measurement()
                else:
                    print("ERR.CODE.SHIT")
                    print(str(fb_scan), " FB SCAN VALUE")
                    self.errors.emit(1, "ERR.CODE.SHIT\n"+str(fb_scan)+" FB SCAN VALUE")
                #END of measurement loop
                #Below is the end of while loop:
                dark = dark - 2
            if motor is not None and motor.idx == 0:
                motor.low_pins()
            if self.params['cRel']:
                console("REL OFF")
                self.relay.toggle(self.relay.OFF)
        except Exception as ex:
            traceback.print_exc()
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
            trig_time_int = self.params['wait']/1000 # convert into seconds
            self.meter.setMeasurementRange(2e-4) # 200 μA range?
            self.current_scale=2e-4 #
            # self.meter.setCurrentAutoRangeLLIM(2e-9) # 2 nA lower limit
            # self.meter.setCurrentAutoRangeULIM(1e-6) # 1 μA upper limit
            self.meter.setMeasurementSpeed(self.params['nplc']) # 0.1 NPLC
            self.meter.setTriggerDelay()  # no parameter is used for zero delay
            self.meter.setCurrentLimit(self.params['limitA'])
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
            time.sleep(1) # one second is enough?
            data = self.meter.fetchArrayData(self.meter.CURR) #
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
            self.final.emit(True)
        except Exception as ex:
            traceback.print_exc()
            print("ERR.CODE.004")
            print(str(ex))
            print("ERROR IN: stop_measurement function")
        pass

    @pyqtSlot()
    def stop(self):
        self._require_stop = True
        self.stop_measurement()
        pass

    def stop_now(self):
        self.errors.emit(-1, 'EXP was cancelled! The current was to big! I >= 0.021 A ( 21 mA )')
        self.stop_measurement()
        print('Overflow was to big!')
        pass