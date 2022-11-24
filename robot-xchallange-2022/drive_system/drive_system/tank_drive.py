from .motor_BLDC import motor_BLDC

import RPi.GPIO as GPIO


class TankDrive:
    def __init__(self,
                 front_left_motor: motor_BLDC, front_righ_motor: motor_BLDC,
                 back_left_motor: motor_BLDC, back_righ_motor: motor_BLDC, brake_pin_left: int, brake_pin_right: int):

        self._front_left_motor = front_left_motor
        self._front_right_motor = front_righ_motor

        self._back_left_motor = back_left_motor
        self._back_right_motor = back_righ_motor

        self._brake_pin_left = brake_pin_left
        self._brake_pin_right = brake_pin_right

        self.TURN_MULTIPLIER = 0.5

        GPIO.setup(self._brake_pin_left, GPIO.OUT)
        GPIO.setup(self._brake_pin_right, GPIO.OUT)

    def drive(self, speed, turn):
        if speed != 0:
            self.TURN_MULTIPLIER = 0.2
        else:
            self.TURN_MULTIPLIER = 0.5

        left_speed = speed + turn * self.TURN_MULTIPLIER
        right_speed = speed - turn * self.TURN_MULTIPLIER

        self._front_left_motor.run(left_speed)
        self._front_right_motor.run(right_speed)

        self._back_left_motor.run(left_speed)
        self._back_right_motor.run(right_speed)

        if abs(left_speed) != 0:
            GPIO.output(self._brake_pin_left, GPIO.HIGH)
        else:
            GPIO.output(self._brake_pin_left, GPIO.LOW)

        if abs(right_speed) != 0:
            GPIO.output(self._brake_pin_right, GPIO.HIGH)
        else:
            GPIO.output(self._brake_pin_right, GPIO.LOW)
