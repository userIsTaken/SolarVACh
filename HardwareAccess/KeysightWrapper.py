from PyQt5 import QtCore, QtGui
from vxi11 import vxi11 as vx

class SourceMeter():
    def __init__(self, _ip_address:str):
        """

        :param _ip_address: TCP/IP address of source meter
        """
        self.Device = vx.Instrument(_ip_address)
        self.ID = self.Device.ask("*IDN?")
        self.ON = "ON"
        self.OFF = "OFF"
        self.bON = True
        self.bOFF = False
        self.CURRENT_MODE = 1
        self.VOLTAGE_MODE = 2
        self.TRIGGER_TIM = 1
        self.TRIGGER_AINT = 0
        self.TRIGGER_BUS = 2
        self.SOURCE_MODE_VOLTS = "VOLT"
        self.SOURCE_MODE_CURR = "CURR"
        self.MEAS_RANGE_AUTO = "AUTO"
        self.MEAS_MODE_CURR = "curr"
        self.MEAS_MODE_VOLT = "volt"
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

        :param _atype:
        :return:
        """
        dataArray = None
        if (_atype.capitalize() in "CURRENT" ):
            dataArray = self.Device.ask(":fetc:arr:curr?")
            pass
        elif (_atype.capitalize() in "VOLTAGE"):
            dataArray = self.Device.ask(":fetc:arr:volt?")
        else:
            dataArray = None
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
        :param mode: curr or volt
        :param on: ON OFF
        :return:
        """
        if str(range) == "AUTO":
            self.write(":sens:"+mode+":rang:auto "+on)
        else:
            self.write(":sens:" + mode + ":rang:auto " + "off")
            self.write(":sens:"+mode+":rang "+str(range))
            pass
        pass
