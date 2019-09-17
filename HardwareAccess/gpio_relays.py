import os
import platform
from Config.confparser import getGPIOip
IP = getGPIOip()
print(IP)
try:
    if 'arm' in platform.machine():
        import gpiozero
    else:
        os.environ['GPIOZERO_PIN_FACTORY'] = "pigpio"
        os.environ['PIGPIO_ADDR'] = IP
        import gpiozero
        from gpiozero.pins.pigpio import PiGPIOFactory
        gpiozero.Device.pin_factory = PiGPIOFactory(IP)
except Exception as ex:
    print('ERR: '+str(ex))
    pass



class RelayToggle():
    def __init__(self, RELAY:str, _ip_address:str = IP):
        """
        :param _ip_address: TCP/IP address of source meter
        """
        self.pin = {'1': 14,
                    '2': 15,
                    '3': 18,
                    '4': 23,
                    '5': 24,
                    '6': 25}

        self.ON = True
        self.OFF = False
        self.relay = gpiozero.OutputDevice(self.pin[RELAY], active_high=False, initial_value=False)
        pass

    def toggle(self, status):
        if status:
            self.relay.on()
        else:
            self.relay.off()
        pass

