#! /usr/bin/python3

# from camera import CameraPublisher
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
        front_left_motor = Motor(True,
                                 Constants.Motors.FRONT_LEFT_MOTOR_PWM_PIN,
                                 Constants.Motors.LEFT_REV_PIN)
        front_right_motor = Motor(False,
                                  Constants.Motors.FRONT_RIGHT_MOTOR_PWM_PIN,
                                  Constants.Motors.RIGHT_REV_PIN)

        back_left_motor = Motor(True,
                                Constants.Motors.BACK_LEFT_MOTOR_PWM_PIN,
                                Constants.Motors.LEFT_REV_PIN)
        back_right_motor = Motor(False,
                                 Constants.Motors.BACK_RIGHT_MOTOR_PWM_PIN,
                                 Constants.Motors.RIGHT_REV_PIN)

        self.speed = 0.0

        self.tank_drive = TankDrive(front_left_motor, front_right_motor,
                                    back_left_motor, back_right_motor)

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
            1)

    def _command_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

    def _cmd_vel_callback(self, msg):
        self.speed = msg.linear.x
        self.get_logger().info('I heard: "%s"' % msg.linear.x)

    def _cmd_joy_callback(self, msg: Joy):
        speed = msg.axes[1] * 10  # 10 is multiplier to make scale from 0-100%
        turn = msg.axes[3] * 10

        self.get_logger().info('speed: ' + str(speed) + '% , turn: ' + str(turn) + "%.")

        self.tank_drive.drive(speed, turn)


# to run joystick node run this commnad in terminal
# ros2 run joy joy_node

def main(args=None):
    rclpy.init(args=args)

    robot = Robot('robot')
    # imagePublisher = CameraPublisher()

    rclpy.spin(robot)
    # rclpy.spin(imagePublisher)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
