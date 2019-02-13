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
        self.buffer = None # nvbuffer1 or nvbuffer2
        # ============================================
        # ============================================
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
        self.CURR = "curr"
        self.VOLT = "volt"
        # ============================================
        pass

    def getIDN(self):
        return self.ID

    def ask(self, cmd:str):
        data = self.Device.ask(cmd)
        return data

    def write(self, cmd:str):
        self.Device.write(cmd)

    def initAcquire(self):
        # measurement:
        # smua.measure.v(smua.nvbuffer1)
        self.write(self.X+'.measure.'+self.mode+'('+self.buffer+')')
        pass

    def fetchArrayData(self, _atype:str):
        '''
        Prints buffer.

        :param _atype:
        :return: buffer
        '''
        buffer = self.ask('printbuffer(1, '+str(self.buffer_size)+', '+self.buffer+')')
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
            self.mode = 'i' # CURRENT MODE
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
        # delay between measurement counts
        # inconsistency with keysight
        pass

    def resetDevice(self):
        self.write("*RST")
        pass

    def setVoltOutValue(self, value):
        # smua.source.levelv = 1
        self.write(self.X+'.source.'+self.source_mode + '='+str(value))
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
        # always auto:
        pass

    def setMeasurementSpeed(self, speed="auto", mode="curr"):
        # nlpc?
        if speed == 'auto':
            self.write(self.X + '.measure.nplc = 10')
        else:
            self.write(self.X+'.measure.nplc ='+str(speed))
        pass

    def setTriggerDelay(self, delay=None):
        # always zero:
        pass

    def close(self):
        self.reset()
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
        if channel == 'smua':
            self.buffer = 'smua.nvbuffer1'
        elif channel == 'smub':
            self.buffer = 'smub.nvbuffer2'
        pass

    def reset(self):
        self.write('reset()')

    def setCurrentLimit(self, limit):
        # smuX.source.limiti
        # limit in A?
        self.write(self.X+'.source.limiti ='+str(limit))
        pass