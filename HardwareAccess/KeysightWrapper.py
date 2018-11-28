from PyQt5 import QtCore, QtGui
from vxi11 import vxi11 as vx

class SourceMeter():
    def __init__(self, _ip_address:str):
        self.Device = vx.Instrument(_ip_address)
        self.ID = self.Device.ask("*IDN?")
        pass

    def getIDN(self):
        return self.ID

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

    