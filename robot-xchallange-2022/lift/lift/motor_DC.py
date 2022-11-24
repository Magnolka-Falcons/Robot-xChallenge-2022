from .constants import Constants

import RPi.GPIO as GPIO


class motor_DC:
    def __init__(self, pinPWM: int, pinREV: int, frequency=Constants.PWM.FREQUENCY, speed=100):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pinPWM, GPIO.OUT)
        GPIO.setup(pinREV, GPIO.OUT)

        self._pinPWM = GPIO.PWM(pinPWM, frequency)
        self._pinREV = pinREV
        self._speed = speed

        self.stop()

    def stop(self):
        self._pinPWM.stop()
        GPIO.output(self._pinREV, GPIO.LOW)

    def forward(self):
        GPIO.output(self._pinREV, GPIO.HIGH)

        self._pinPWM.start(self._speed)

    def reverse(self):
        GPIO.output(self._pinREV, GPIO.LOW)

        self._pinPWM.start(self._speed)

    def drive(self, speed):
        if speed > 100:
            speed = 100

        if speed > 0:
            GPIO.output(self._pinREV, GPIO.HIGH)
            self._pinPWM.start(speed)
        elif speed < 0:
            GPIO.output(self._pinREV, GPIO.LOW)
            self._pinPWM.start(abs(speed))
        else:
            self.stop()
