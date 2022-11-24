#! /usr/bin/python3

from .motor_BLDC import motor_BLDC
from .tank_drive import TankDrive
from .constants import Constants

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class Robot(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("%s is starting..." % name)
        front_left_motor = motor_BLDC(True,
                                      Constants.Motors.FRONT_LEFT_MOTOR_PWM_PIN,
                                      Constants.Motors.LEFT_REV_PIN)
        front_right_motor = motor_BLDC(True,
                                       Constants.Motors.FRONT_RIGHT_MOTOR_PWM_PIN,
                                       Constants.Motors.RIGHT_REV_PIN)

        back_left_motor = motor_BLDC(True,
                                     Constants.Motors.BACK_LEFT_MOTOR_PWM_PIN,
                                     Constants.Motors.LEFT_REV_PIN)
        back_right_motor = motor_BLDC(True,
                                      Constants.Motors.BACK_RIGHT_MOTOR_PWM_PIN,
                                      Constants.Motors.RIGHT_REV_PIN)

        self.speed = 0.0

        self.SPEED_MULTIPLIER = 0.45

        self.last_speed = None
        self.last_turn = None

        self.tank_drive = TankDrive(front_left_motor, front_right_motor,
                                    back_left_motor, back_right_motor,
                                    Constants.Motors.LEFT_BRAKE_PIN, Constants.Motors.RIGHT_BRAKE_PIN)

        self._command = self.create_subscription(
            String,
            "command",
            self._command_callback,
            1)

        self._cmd_vel_subscription = self.create_subscription(
            Twist,
            "cmd_vel",
            self._cmd_vel_callback,
            2)

        self._cmd_joy_subscription = self.create_subscription(
            Joy,
            "joy",
            self._cmd_joy_callback,
            1)

    def _command_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

    def _cmd_vel_callback(self, msg):
        speed = msg.linear.x * 100  # 10 is multiplier to make scale from 0-100%
        turn = msg.linear.y * 100
        self.tank_drive.drive(speed, turn)
        self.get_logger().info('Speed: ' + str(speed) + '% , Turn: ' + str(turn) + "%.")

    def _cmd_joy_callback(self, msg: Joy):
        speed = msg.axes[1] * 100  # 10 is multiplier to make scale from 0-100%
        turn = msg.axes[3] * 100

        if speed != self.last_speed or turn != self.last_turn:
            self.get_logger().info('Speed: ' + str(speed) + '% , Turn: ' + str(turn) + "%.")
            self.tank_drive.drive(speed * self.SPEED_MULTIPLIER, turn)
            self.last_speed = speed
            self.last_turn = turn


# to run joystick node run this commnad in terminal
# ros2 run joy joy_node

def main(args=None):
    rclpy.init(args=args)

    robot = Robot('robot')
    try:
        robot.get_logger().info('Beginning client, shut down with CTRL-C')
        rclpy.spin(robot)
    except KeyboardInterrupt:
        robot.get_logger().info('Keyboard interrupt, shutting down.\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
