import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

from .constants import Constants
from .motor_DC import motor_DC


class Lift_node(Node):
    def __init__(self, name):
        super().__init__(name)

        self.get_logger().info("%s is starting..." % name)

        self.lift_motor = motor_DC(Constants.Motors.PWM_PIN_LIFT,
                                   Constants.Motors.REV_PIN_LIFT, default_speed=100)
        self.gripper_motor = motor_DC(Constants.Motors.PWM_PIN_GRIPPER,
                                      Constants.Motors.REV_PIN_GRIPPER, default_speed=5)

        self._cmd_joy_subscription = self.create_subscription(
            Joy,
            "joy",
            self._cmd_joy_callback,
            1)

        self.lift_motor.set_default_speed(100)

    def _cmd_joy_callback(self, msg: Joy):
        self.lift_callback(msg)
        self.gripper_callback(msg)

    def lift_callback(self, msg: Joy):
        if (msg.buttons[4] == 1):
            self.gripper_motor.drive(100)
        elif (msg.buttons[5] == 1):
            self.gripper_motor.drive(-100)
        else:
            self.lift_motor.stop()

    def gripper_callback(self, msg: Joy):
        if msg.buttons[0] == 1:
            self.lift_motor.set_default_speed(10)
        else:
            self.lift_motor.set_default_speed(5)
        SPEED_MULTIPLIER = 1

        if (msg.axes[2] <= 0.8):
            speed = -0.5 * (msg.axes[2]) + 0.5
            self.gripper_motor.drive(speed * 100 * SPEED_MULTIPLIER)

        elif (msg.axes[5] <= 0.8):
            speed = -0.5 * (msg.axes[5]) + 0.5
            self.gripper_motor.drive(-speed * 100 * SPEED_MULTIPLIER)
        else:
            self.gripper_motor.stop()


def main(args=None):
    rclpy.init(args=args)

    lift_node = Lift_node('lift_node')
    try:
        lift_node.get_logger().info('Beginning client, shut down with CTRL-C')
        rclpy.spin(lift_node)
    except KeyboardInterrupt:
        lift_node.get_logger().info('Keyboard interrupt, shutting down.\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
