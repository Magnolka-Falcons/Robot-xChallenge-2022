from motor import Motor


class TankDrive:
    def __init__(self, left_motor: Motor, righ_motor: Motor):
        self._left_motor = left_motor
        self._right_motor = righ_motor

    def drive(self, speed, turn):
        left_motor_speed = speed + turn * 0.3
        right_motor_speed = speed - turn * 0.3

        self._left_motor.run(left_motor_speed)
        self._right_motor.run(right_motor_speed)
