import time
import platform
local = True
if 'arm' in platform.machine():
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    local = True
    print('local mode')
else:
    import spur
    local = False
    print('remote mode')


class Motor():
    def __init__(self):
        self.IP = None
        self.GpioPins = [4, 17, 27, 22] # pinout
        self.StepSequence = list(range(0, 8))
        self.wait_time = 0.001
        self.Shell = None
        self.Status = False # if false - it is opened, true - closed
        self.Local = local
        self.idx = 0



    def set_ip(self, IP):
        self.IP = IP

    def setup(self):
        try:
            if self.Local:
                for pin in self.GpioPins:
                    GPIO.setup(pin, GPIO.OUT)  # Set pin to output
                    GPIO.output(pin, False)  # Set pin to low ("False")

        except Exception as ex:
            print(str(ex))
            pass

        self.StepSequence[0] = [self.GpioPins[0]]
        self.StepSequence[1] = [self.GpioPins[0], self.GpioPins[1]]
        self.StepSequence[2] = [self.GpioPins[1]]
        self.StepSequence[3] = [self.GpioPins[1], self.GpioPins[2]]
        self.StepSequence[4] = [self.GpioPins[2]]
        self.StepSequence[5] = [self.GpioPins[2], self.GpioPins[3]]
        self.StepSequence[6] = [self.GpioPins[3]]
        self.StepSequence[7] = [self.GpioPins[3], self.GpioPins[0]]
        if not self.Local:
            self.Shell = spur.SshShell([self.IP, 'a310', 'a310'])
        pass

    def move_motor_ccw(self, steps=256):
        status = False
        if not self.Local:
            cmd = ['python3','stp_mot.py','-s '+str(steps),'-cc']
            c = self.Shell.run(cmd)
            if c == 0:
                status = True
        elif self.Local:
            stepsRemaining = steps
            self.StepSequence.reverse()
            #seq = seq.reverse()
            while stepsRemaining > 0:
                for pinList in self.StepSequence:
                    for pin in self.GpioPins:
                        if pin in pinList:
                            GPIO.output(pin, True)
                        else:
                            GPIO.output(pin, False)
                        # PrintStatus(pinList)
                    time.sleep(self.wait_time)
                stepsRemaining -= 1
            status = True
        else:
            status = False
            print('Something wrong with the control of a stepper motor')
        return status

    def move_motor_cw(self, steps=256):
        status = False
        if not self.Local:
            cmd = ['python3', 'stp_mot.py', '-s ' + str(steps)]
            c = self.Shell.run(cmd)
            if c ==0:
                status = True
        elif self.Local:
            stepsRemaining = steps
            seq = self.StepSequence
            while stepsRemaining > 0:
                for pinList in seq:
                    for pin in self.GpioPins:
                        if pin in pinList:
                            GPIO.output(pin, True)
                        else:
                            GPIO.output(pin, False)
                        # PrintStatus(pinList)
                    time.sleep(self.wait_time)
                stepsRemaining -= 1
            status = True
        else:
            status = False
            print('Something wrong with the control of a stepper motor')
        return status

    def low_pins(self):
        for i in self.GpioPins:
            GPIO.output(i, False)