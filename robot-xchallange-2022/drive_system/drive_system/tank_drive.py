from .motor import Motor


class TankDrive:
    def __init__(self,
                 front_left_motor: Motor, front_righ_motor: Motor,
                 back_left_motor: Motor, back_righ_motor: Motor):

        self._front_left_motor = front_left_motor
        self._front_right_motor = front_righ_motor

        self._back_left_motor = back_left_motor
        self._back_right_motor = back_righ_motor

    def drive(self, speed, turn):
        left_speed = speed + turn * 0.6
        right_speed = speed - turn * 0.6

        self._front_left_motor.run(left_speed)
        self._front_right_motor.run(right_speed)

        self._back_left_motor.run(left_speed)
        self._back_right_motor.run(right_speed)
