import cv2
import numpy as np

import threading
from collections import deque

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage

from cv_bridge import CvBridge


class CameraNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("%s is starting..." % name)

        self.publisher_ = self.create_publisher(
            CompressedImage,
            'camera_node',
            1)
        timer_period = 1/30  # seconds/
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

        self.camera = cv2.VideoCapture(0)
        self.frame = deque(maxlen=1)

        blank_image = np.zeros((640, 480, 3), np.uint8)
        self.frame.append(blank_image)

        self.bridge = CvBridge()

        self.camera_thread = threading.Thread(
            target=self.update_camera, args=())
        self.camera_thread.daemon = True
        self.camera_thread.start()

    # def timer_callback(self):
    #     msg = String()
    #     msg.data = 'Hello World: %d' % self.i
    #     self.publisher_.publish(msg)
    #     self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1

    def timer_callback(self):
        print("cos")
        self.publisher_.publish(
            self.bridge.cv2_to_compressed_imgmsg(self.frame[-1]))

        self.get_logger().info("Image sent")

    def update_camera(self):
        frame = None
        while True:
            if self.camera.isOpened():
                ret, frame = self.camera.read()
            else:
                self.get_logger().error('Camera unavavible!')

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame.append(frame)


def main():
    rclpy.init()

    imagePublisher = CameraNode('camera_node')
    try:
        imagePublisher.get_logger().info('Beginning client, shut down with CTRL-C')
        rclpy.spin(imagePublisher)
    except KeyboardInterrupt:
        imagePublisher.get_logger().info('Keyboard interrupt, shutting down.\n')

    rclpy.shutdown()


if __name__ == '__main__':
    main()
