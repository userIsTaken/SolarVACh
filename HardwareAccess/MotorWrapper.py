import time
import platform
# import RPi.GPIO as GPIO
# import argparse
# GPIO.setwarnings(False)
local = True
if 'arm' in platform.machine():
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    local = True

else:
    import spur
    local = False


class Motor():
    def __init__(self):
        self.IP = None
        self.GpioPins = [4, 17, 27, 22]

    def set_ip(self, IP):
        self.IP = IP

    def move_motor_ccw(self, steps=256):
        if not local:
            pass
        elif local:
            pass
        else:
            print('Something wrong with the control of a stepper motor')
        pass

    def move_motor_cw(self, steps=256):
        if not local:
            pass
        elif local:
            pass
        else:
            print('Something wrong with the control of a stepper motor')
        pass

    def low_pins(self):
        pass