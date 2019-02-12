from PyQt5 import QtCore, QtGui
from vxi11 import vxi11 as vx

class SourceMeter_KTHL():
    def __init__(self, _ip_address:str):
        """

        :param _ip_address: TCP/IP address of source meter
        """
        self.Device = vx.Instrument(_ip_address)
        self.ID = self.Device.ask("*IDN?")
        self.buffer_size=None
        self.A = 'smua'
        self.B = 'smub'
        self.X = None # smu active channel
        self.mode = None # measurement mode - i, v, r ?
        self.source_mode = None # leveli or levelv, i or v?
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
        '''
        Prints buffer.

        :param _atype:
        :return: buffer
        '''
        buffer = self.ask('printbuffer(1, )'+str(self.buffer_size)+', '+self.X+'.nvbuffer1)')
        return buffer
        pass

    def enableVoltageOutput(self, _status:bool):
        if _status:
            self.write(self.X+'.source.output ='+str(self.X+'.OUTPUT_ON'))
            pass
        else:
            self.write(self.X + '.source.output =' + str(self.X + '.OUTPUT_OFF'))
            pass
        pass

    def enableAmmeterInput(self, _status:bool):
        pass

    def setMeasurementMode(self, mode:int):
        if (mode == 1):
            self.mode = 'i'
        elif (mode == 2):
            self.mode = 'v'  # VOLTAGE MODE
        else:
            pass
        pass

    def setTriggerSource(self, source:int):
        pass

    def setTriggerCounts(self, counts):
        # inconsistency between keysight and keithley
        #  smuX.measure.count
        self.write(self.X+'.measure.count = '+str(counts))
        pass

    def setTriggerTimerInterval(self, interval):
        pass

    def resetDevice(self):
        self.write("*RST")
        pass

    def setVoltOutValue(self, value):
        pass

    def setSourceOutputMode(self, mode):
        if str(mode).lower() in 'current':
            self.source_mode = 'leveli'
        elif str(mode).lower() in 'voltage':
            self.source_mode = 'levelv'
        else:
            pass
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

    def setCurrentAutoRangeLLIM(self, llim):
        pass

    def setCurrentAutoRangeULIM(self, ulim):
        pass

    def setCurrentSensorRange(self, range):
        pass

    def getCurrentSensorRange(self):
        pass

    def setBufferSize(self, size):
        self.buffer_size = size

    def setChannel(self, channel):
        self.X = channel
        pass