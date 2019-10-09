from PyQt5 import QtCore, QtGui
import os, sys

class Device_USB():
    def __init__(self, _usb:str, _line:str = "\r\n"):
        self._dev = _usb
        self._dev_file = open(self._dev, '+', buffering=0, newline=_line)
        pass

    def ask(self, cmd:str):
        self._write(cmd)
        txt = self._read()
        return txt
        pass

    def write(self, cmd:str):
        self._write(cmd)
        pass

    def _write(self, cmd:str):
        self._dev_file.write(cmd)
        #self._dev_file.writelines(cmd)
        pass

    def _read(self):
        answ = self._dev_file.readline()
        return answ
        pass

    def _close_f(self):
        self._dev_file.close()

class SourceMeter_USB():
    def __init__(self, _usb:str, _line:str="\r\n"):
        """

        :param _usb: /dev/usbtmcX link of source meter, where X is 0, 1, 2, ...
        """
        self.Device = Device_USB(_usb)
        self.ID = self.Device.ask("*IDN?")
        self.ON = "ON"
        self.OFF = "OFF"
        self.bON = True
        self.bOFF = False
        self.CURRENT_MODE = 1
        self.VOLTAGE_MODE = 2
        # Trigger sources:
        self.TRIGGER_TIM = 1
        self.TRIGGER_AINT = 0
        self.TRIGGER_BUS = 2
        # end of trigger sources
        self.SOURCE_MODE_VOLTS = "VOLT"
        self.SOURCE_MODE_CURR = "CURR"
        self.MEAS_RANGE_AUTO = "AUTO"
        self.MEAS_MODE_CURR = "curr"
        self.MEAS_MODE_VOLT = "volt"
        self.CURR="curr"
        self.VOLT="volt"
        pass

    def getIDN(self):
        return self.ID

    def ask(self, cmd:str):
        data = self.Device.ask(cmd)
        return data

    def write(self, cmd:str):
        self.Device.write(cmd)

    def initAcquire(self):
        self.Device.write(":init:acq")
        pass

    def fetchArrayData(self, _atype:str):
        """

        :param _atype: curr or volt, it will work even by passing c or v.
        :return:
        """
        dataArray = None
        if (_atype.upper() in "CURRENT" ):
            dataArray = self.Device.ask(":fetc:arr:curr?")
            pass
        elif (_atype.upper() in "VOLTAGE"):
            dataArray = self.Device.ask(":fetc:arr:volt?")
        else:
            dataArray = "fcuk"
        return dataArray

    def enableVoltageOutput(self, _status:bool):
        """

        :param _status:
        :return:
        """
        if(_status):
            self.write(":OUTP ON")
        elif (not _status):
            self.write(":OUTP OFF")
        else:
            pass
        pass

    def enableAmmeterInput(self, _status:bool):
        """

        :param _status:
        :return:
        """
        if (_status):
            self.write(":INP ON")
        elif (not _status):
            self.write(":INP OFF")
        else:
            pass
        pass

    def setMeasurementMode(self, mode:int):
        """

        :param mode:
        :return:
        """
        if(mode == 1):
            self.write(":SENS:FUNC \"CURR\"") #  CURRENT MODE
        elif (mode == 2):
            self.write(":SENS:FUNC \"VOLT\"") #  VOLTAGE MODE
        else:
            pass
        pass

    def setTriggerSource(self, source:int):
        """

        :param source:
        :return:
        """
        if source == 1: #TIMER TRIGGER
            self.write(":trig:sour tim")
            pass
        elif source == 0:
            self.write(":trig:sour aint")
            pass
        elif source == 2:
            self.write(":trig:sour bus")
        else:
            pass
        pass

    def setTriggerCounts(self, counts):
        """

        :param counts:
        :return:
        """
        self.write(":trig:coun "+str(counts))
        pass

    def setTriggerTimerInterval(self, interval):
        """

        :param interval:
        :return:
        """
        self.write(":trig:tim "+str(interval))
        pass

    def resetDevice(self):
        self.write("*RST")
        pass

    def setVoltOutValue(self, value):
        """

        :param value:
        :return:
        """
        self.write(":SOUR:VOLT "+str(value))
        pass

    def setSourceOutputMode(self, mode):
        """

        :param mode:
        :return:
        """
        self.write(":SOUR:FUNC:MODE "+str(mode))
        pass

    def setMeasurementRange(self, range, mode="curr", on="ON"):
        """

        :param range: AUTO or value
        :param mode: curr or volt, default : current
        :param on: ON OFF, default : ON
        :return:
        """
        if str(range).upper() == "AUTO":
            self.write(":sens:"+mode+":rang:auto "+on)
        else:
            self.write(":sens:" + mode + ":rang:auto " + "off")
            self.write(":sens:"+mode+":rang "+str(range))
            pass
        pass

    def setMeasurementSpeed(self, speed="auto", mode="curr"):
        """

        :param speed: auto, 0.001, 0.1, 1, 10, it is explained deeper in doc's
        :param mode: curr. volt
        :return:
        """
        print('keysight nplc ', speed)
        if speed is not None:
            if (str(speed).lower() in "auto"):
                self.write(":sens:"+mode+":nplc:auto on")
            else:
                self.write(":sens:"+mode+":nplc:auto off")
                self.write(":sens:"+mode+":nplc "+str(speed))
        else:
            self.write(":sens:" + mode + ":nplc:auto on")
        pass

    def setTriggerDelay(self, delay=None):
        """

        :param delay: None or delay in seconds
        :return:
        """
        if delay is None:
            self.write(":trig:acq:del 0")
        else:
            self.write(":trig:acq:del "+str(delay))
        pass

    def close(self):
        self.Device.close()
        pass

    # ioObj.WriteString(":sens:curr:rang:auto:llim 2e-9")

    def setCurrentAutoRangeLLIM(self, llim):
        self.write(":sens:curr:rang:auto:llim "+str(llim))
        pass

    def setCurrentAutoRangeULIM(self, ulim):
        self.write(":sens:curr:rang:auto:ulim " + str(ulim))
        pass

    def setCurrentSensorRange(self, range):
        self.write(":sens:curr:rang " + str(range))
        pass


    def setCurrentLimit(self, limit):
        # smuX.source.limiti
        # limit in A?
        # if float(limit) <= 0:
        #     self.write(':SOUR:VOLT:RLIM:STAT 0')
        # else:
        #     self.write(':SOUR:VOLT:RLIM:STAT 1')
        pass

    def getCurrentSensorRange(self):
        answer = self.Device.ask(":sens:curr:rang?")
        return answer
        pass

    def clearBuffer(self):
        pass