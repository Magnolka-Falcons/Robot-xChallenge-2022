from .constants import Constants

import RPi.GPIO as GPIO


class Motor:
    def __init__(self, reversed: bool, pinFwdPwm: int, pinRev: int, frequency=Constants.PWM.FREQUENCY, maxSpeed=100):
        """
         Create motor object.

        `reversed`- If motor is spinning wrong way, set True.
        `frequency`- PWM frequency
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pinFwdPwm,  GPIO.OUT)
        GPIO.setup(pinRev, GPIO.OUT)

        self._pinRev = pinRev
        self._reversed = reversed

        self._frequency = frequency
        self._maxSpeed = maxSpeed
        self._pwm = GPIO.PWM(pinFwdPwm, frequency)
        self.stop()

    def stop(self):
        self._pwm.stop()

    def run(self, speed=None):

        if speed == None:
            speed = self._maxSpeed

        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        print(speed)

        if self._reversed:
            speed = speed*-1
        print(self._reversed)

        if speed < 0:
            GPIO.output(self._pinRev, GPIO.HIGH)
        else:
            GPIO.output(self._pinRev, GPIO.LOW)

        self._pwm.start(abs(speed))

    def driveBackwards(self, motorPin1, motorPin2):
        GPIO.setup(motorPin1,  GPIO.OUT)
        GPIO.setup(motorPin2,  GPIO.OUT)

        self.output(motorPin1, True)
        self.output(motorPin2, True)

    def driveForward(self, motorPin1, motorPin2):
        GPIO.setup(motorPin1,  GPIO.OUT)
        GPIO.setup(motorPin2,  GPIO.OUT)

        self.output(motorPin1, True)
        self.output(motorPin2, False)
