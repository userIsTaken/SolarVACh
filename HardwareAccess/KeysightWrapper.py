from PyQt5 import QtCore, QtGui
from vxi11 import vxi11 as vx

class SourceMeter():
    def __init__(self, _ip_address:str):
        self.Device = vx.Instrument(_ip_address)
        self.ID = self.Device.ask("*IDN?")
        self.ON = True
        self.OFF = False
        self.CURRENT_MODE = 1
        self.VOLTAGE_MODE = 2
        self.TRIGGER_TIM = 1
        self.TRIGGER_AINT = 0
        self.TRIGGER_BUS = 2
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
        if(_status):
            self.write(":OUTP ON")
        elif (not _status):
            self.write(":OUTP OFF")
        else:
            pass
        pass

    def enableAmmeterInput(self, _status:bool):
        if (_status):
            self.write(":INP ON")
        elif (not _status):
            self.write(":INP OFF")
        else:
            pass
        pass

    def setMeasurementMode(self, mode:int):
        if(mode == 1):
            self.write(":SENS:FUNC \"CURR\"") #  CURRENT MODE
        elif (mode == 2):
            self.write(":SENS:FUNC \"VOLT\"") #  VOLTAGE MODE
        else:
            pass
        pass

    def setTriggerSource(self, source:int):
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
        self.write(":trig:coun "+str(counts))
        pass

    def setTriggerTimerInterval(self, interval):
        self.write(":trig:tim "+str(interval))
        pass