import os
import platform
if 'arm' in platform.machine():
    # os.environ['GPIOZERO_PIN_FACTORY'] = "pigpio"
    # os.environ['PIGPIO_ADDR'] = "192.168.0.104"
    import gpiozero
    from pigpio import PiGPIOFactory



class RelayToggle():
    def __init__(self, RELAY:str, _ip_address:str = '192.168.0.104'):
        """
        :param _ip_address: TCP/IP address of source meter
        """
        self.pin = {'1': 5,
                    '2': 6,
                    '3': 13,
                    '4': 19,
                    '5': 26,
                    '6': 12}
        gpiozero.Device.pin_factory = PiGPIOFactory(_ip_address)
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
