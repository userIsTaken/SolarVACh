import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory



class RelayToggle():
    def __init__(self, _ip_address:str = '192.168.0.104'):
        """

        :param _ip_address: TCP/IP address of source meter
        """
        self.gpiozero.Device.pin_factory = PiGPIOFactory(_ip_address)
        self.RELAY_1 = 5
        self.RELAY_2 = 6
        self.RELAY_3 = 13
        self.RELAY_4 = 19
        self.RELAY_5 = 26
        self.RELAY_6 = 12
        self.ON = True
        self.OFF = False
        self.relay = None
        pass

    def set_relay(self, RELAY_PIN):
        self.relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)
        pass

    def toggle_relay(self, status):
        if status:
            self.relay.on()
        else:
            self.relay.off()
        pass
