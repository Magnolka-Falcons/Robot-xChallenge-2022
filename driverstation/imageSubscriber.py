import rclpy
from rclpy.node import Node

from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2


class imageSubscriber(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.subscription = self.create_subscription(
            CompressedImage,
            'camera_node',
            self.listener_callback,
            1)
        self.subscription

        self.br = CvBridge()

        window_name = "camera"

        cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
        cv2.setWindowProperty(
            window_name, cv2.WINDOW_KEEPRATIO, cv2.WINDOW_KEEPRATIO)

    def listener_callback(self, data):
        self.get_logger().info('Receiving video frame')

        current_frame = self.br.compressed_imgmsg_to_cv2(data)
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        current_frame = cv2.flip(current_frame, 0)
        cv2.imshow("camera", current_frame)

        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)

    image_subscriber = imageSubscriber()

    rclpy.spin(image_subscriber)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
