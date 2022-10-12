from constants import Constants

import RPi.GPIO as GPIO


class Motor:
    def __init__(self, pinFwd, pinRev, frequency=Constants.PWM.FREQUENCY, maxSpeed=100):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pinFwd,  GPIO.OUT)
        GPIO.setup(pinRev, GPIO.OUT)

        self._frequency = frequency
        self._maxSpeed = maxSpeed
        self._pwmFwd = GPIO.PWM(pinFwd, frequency)
        self._pwmRev = GPIO.PWM(pinRev, frequency)
        self.stop()

    def stop(self):

        #self._pwmFwd.start(0)
        #self._pwmRev.start(0)

        self._pwmFwd.stop()
        self._pwmRev.stop()

    def run(self, speed=None):
        if speed == None:
            speed = self._maxSpeed

        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100

        print(speed)

        if speed < 0:
            self._pwmRev.start(speed * -1)
            self._pwmRev.start(0)
        else:
            self._pwmFwd.start(speed)
            self._pwmRev.start(0)

    def driveBackwards(self, motorPin1, motorPin2):
        GPIO.setup(motorPin1,  GPIO.OUT)
        GPIO.setup(motorPin2,  GPIO.OUT)

        self.output(motorPin1, true)
        self.output(motorPin2, true)

    def driveForward(self, motorPin1, motorPin2):
        GPIO.setup(motorPin1,  GPIO.OUT)
        GPIO.setup(motorPin2,  GPIO.OUT)

        self.output(motorPin1, true)
        self.output(motorPin2, false)
        