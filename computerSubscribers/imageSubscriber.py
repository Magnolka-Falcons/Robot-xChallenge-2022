import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2

class imageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            'camera_node',
            self.listener_callback,
            1)
        self.subscription

        self.br = CvBridge()

    def listener_callback(self, data):
        self.get_logger().info('Receiving video frame')

        current_frame = self.br.imgmsg_to_cv2(data)

        cv2.imgshow("camera", current_frame)

        cv2.waitKey(1)

    def main(args=None):
        rclpy.init(args=args)

        image_subscriber = imageSubscriber()

        rclpy.spin(image_subscriber)

        rclpy.shutdown()

    if __name__ == '__main__':
        main()
