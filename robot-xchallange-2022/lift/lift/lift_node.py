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

        self.lift_motor = motor_DC(Constants.Motors.PWM_PIN,
                                   Constants.Motors.REV_PIN, speed=10)

        self._cmd_joy_subscription = self.create_subscription(
            Joy,
            "joy",
            self._cmd_joy_callback,
            1)

    def _cmd_joy_callback(self, msg: Joy):
        self.get_logger().info("Trigger info:" +
                               str(msg.axes[5]) + str(msg.axes[2]))
        if (msg.axes[2] <= 0.8):
            self.lift_motor.forward()
        elif (msg.axes[5] <= 0.8):
            self.lift_motor.reverse()
        else:
            self.lift_motor.stop()


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
