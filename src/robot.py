#! /usr/bin/python3

from motor import Motor
from tank_drive import TankDrive
from constants import Constants

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class Robot(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("%s is starting" % name)

        self.speed = 0.0

        left_motor = Motor(Constants.Motors.LEFT_MOTOR_FWD_PWM_PIN,
                           Constants.Motors.LEFT_MOTOR_REV_PWM_PIN)
        right_motor = Motor(Constants.Motors.RIGHT_MOTOR_FWD_PWM_PIN,
                            Constants.Motors.RIGHT_MOTOR_REV_PWM_PIN)

        self.tank_drive = TankDrive(left_motor, right_motor)

        self._command = self.create_subscription(
            String,
            "command",
            self._command_callback,
            10)

        self._cmd_vel_subscription = self.create_subscription(
            Twist,
            "cmd_vel",
            self._cmd_vel_callback,
            2)

        self._cmd_joy_subscription = self.create_subscription(
            Joy,
            "joy",
            self._cmd_joy_callback,
            2)

    def _command_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

    def _cmd_vel_callback(self, msg):
        self.speed = msg.linear.x
        self.get_logger().info('I heard: "%s"' % msg.linear.x)

    def _cmd_joy_callback(self, msg: Joy):
        speed = msg.axes[1]
        turn = msg.axes[3]

        self.get_logger().info('speed: ' + str(speed) + ', turn: ' + str(turn))

        self.tank_drive.drive(speed, turn)


def main(args=None):
    rclpy.init(args=args)

    robot = Robot('robot')

    rclpy.spin(robot)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
