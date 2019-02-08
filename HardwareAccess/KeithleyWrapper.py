from PyQt5 import QtCore, QtGui
from vxi11 import vxi11 as vx

class SourceMeter_KTHL():
    def __init__(self, _ip_address:str):
        """

        :param _ip_address: TCP/IP address of source meter
        """
        self.Device = vx.Instrument(_ip_address)
        self.ID = self.Device.ask("*IDN?")
        # self.ON = "ON"
        # self.OFF = "OFF"
        # self.bON = True
        # self.bOFF = False
        # self.CURRENT_MODE = 1
        # self.VOLTAGE_MODE = 2
        # # Trigger sources:
        # self.TRIGGER_TIM = 1
        # self.TRIGGER_AINT = 0
        # self.TRIGGER_BUS = 2
        # # end of trigger sources
        # self.SOURCE_MODE_VOLTS = "VOLT"
        # self.SOURCE_MODE_CURR = "CURR"
        # self.MEAS_RANGE_AUTO = "AUTO"
        # self.MEAS_MODE_CURR = "curr"
        # self.MEAS_MODE_VOLT = "volt"
        # self.CURR="curr"
        # self.VOLT="volt"
        pass

    def getIDN(self):
        return self.ID

    def ask(self, cmd:str):
        data = self.Device.ask(cmd)
        return data

    def write(self, cmd:str):
        self.Device.write(cmd)

    def initAcquire(self):

        pass

    def fetchArrayData(self, _atype:str):
        pass

    def enableVoltageOutput(self, _status:bool):
        pass

    def enableAmmeterInput(self, _status:bool):
        pass

    def setMeasurementMode(self, mode:int):
        pass

    def setTriggerSource(self, source:int):
        pass

    def setTriggerCounts(self, counts):
        pass

    def setTriggerTimerInterval(self, interval):
        pass

    def resetDevice(self):
        self.write("*RST")
        pass

    def setVoltOutValue(self, value):
        pass

    def setSourceOutputMode(self, mode):
        pass

    def setMeasurementRange(self, range, mode="curr", on="ON"):
        pass

    def setMeasurementSpeed(self, speed="auto", mode="curr"):
        pass

    def setTriggerDelay(self, delay=None):
        pass

    def close(self):
        self.Device.close()
        pass

    # ioObj.WriteString(":sens:curr:rang:auto:llim 2e-9")

    def setCurrentAutoRangeLLIM(self, llim):
        pass

    def setCurrentAutoRangeULIM(self, ulim):
        pass

    def setCurrentSensorRange(self, range):
        pass

    # GET functions:
    def ask(self, cmd):
        answer = self.Device.ask(cmd)
        return answer
        pass

    def getCurrentSensorRange(self):
        pass