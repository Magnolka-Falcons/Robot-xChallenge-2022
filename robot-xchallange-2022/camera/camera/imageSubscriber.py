import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class imageSubscriber(Node):
    def init(self):
        super().init('camera_node')
        self.subscription = self.create_subscription(
            Image,
            'camera_node',
            self.listener_callback,
            1)
        self.subscription

        self.br = CvBridge()
        print("halo")

    def listener_callback(self, data):
        self.get_logger().info('Receiving video frame')

        current_frame = self.br.imgmsg_to_cv2(data)

        cv2.imgshow("camera", current_frame)

        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)

    camera_node = imageSubscriber()

    rclpy.spin(camera_node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()


# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String


# class MinimalSubscriber(Node):

#     def __init__(self):
#         super().__init__('minimal_subscriber')
#         self.subscription = self.create_subscription(
#             String,
#             'camera_node',
#             self.listener_callback,
#             10)
#         self.subscription  # prevent unused variable warning

#     def listener_callback(self, msg):
#         self.get_logger().info('I heard: "%s"' % msg.data)


# def main(args=None):
#     rclpy.init(args=args)

#     minimal_subscriber = MinimalSubscriber()

#     rclpy.spin(minimal_subscriber)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_subscriber.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
