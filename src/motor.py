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

    def driveBack(self, pinPwm1, pinPwm2, frequency=Constants.PWM.FREQUENCY): #name these pwm to your liking
        GPIO.setup(pinPwm1,  GPIO.OUT)
        GPIO.setup(pinPwm2, GPIO.OUT)

        self.pwm1 = GPIO.PWM(pinPwm1, frequency)
        self.pwm2 = GPIO.PWM(pinPwm2, frequency)

        self.pwm1.start(1)
        self.pwm2.start(1)

    def driveStraight(self, pinPwm1, pinPwm2, frequency=Constants.PWM.FREQUENCY):
        GPIO.setup(pinPwm1,  GPIO.OUT)
        GPIO.setup(pinPwm2, GPIO.OUT)

        self.pwm1 = GPIO.PWM(pinPwm1, frequency)
        self.pwm2 = GPIO.PWM(pinPwm2, frequency)

        self.pwm1.start(1)
        self.pwm2.start(0)
        