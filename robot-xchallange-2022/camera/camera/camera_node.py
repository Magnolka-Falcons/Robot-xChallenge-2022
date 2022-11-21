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

        VIDEO_CAPTURE_ID = 0

        self.publisher_ = self.create_publisher(
            CompressedImage,
            'camera_node',
            1)
        timer_period = 1/120  # seconds/
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.camera = cv2.VideoCapture(VIDEO_CAPTURE_ID, cv2.CAP_V4L)
        self.frame = deque(maxlen=1)

        blank_image = np.zeros((480, 848, 3), np.uint8)
        self.frame.append(blank_image)

        self.bridge = CvBridge()

        self.camera_thread = threading.Thread(
            target=self.update_camera, args=())
        self.camera_thread.daemon = True
        self.camera_thread.start()

    def timer_callback(self):
        self.get_logger().info("Sending image")
        self.publisher_.publish(
            self.bridge.cv2_to_compressed_imgmsg(self.frame[-1]))

        self.get_logger().info("Image sent")

    def update_camera(self):
        frame = None
        while True:
            if self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    scale_percent = 100  # percent of original size
                    width = int(frame.shape[1] * scale_percent / 100)
                    height = int(frame.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    frame = cv2.resize(
                        frame, dim, interpolation=cv2.INTER_AREA)
                else:
                    self.get_logger().error('Frame can\'t be read!')
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
