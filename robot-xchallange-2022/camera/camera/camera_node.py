import cv2
import numpy as np

import datetime
from time import time

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

        RECORD = True
        self.VIDEO_SAVE_FREQUENCY = 10

        self.publisher_ = self.create_publisher(
            CompressedImage,
            'camera_node',
            1)
        timer_period = 1/20  # seconds/
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

        self.video_thread = threading.Thread(
            target=self.record_video, args=())
        self.video_thread.daemon = True

        if RECORD:
            self.video_thread.start()

    def record_video(self):
        camera_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        camera_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

        video_out = cv2.VideoWriter('/home/ubuntu/robot_ros/Robot-xChallange-2022/video/Video_' + str(datetime.datetime.now()) + '.avi',
                                    cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (int(camera_width), int(camera_height)))
        last_time = time()
        while time() - last_time < self.VIDEO_SAVE_FREQUENCY:
            frame = cv2.cvtColor(self.frame[-1], cv2.COLOR_BGR2RGB)
            video_out.write(frame)
        video_out.release()
        self.get_logger().info('Vidoe saved!')

        threading.Thread(
            target=self.record_video, args=()).start()

    def timer_callback(self):
        self.publisher_.publish(
            self.bridge.cv2_to_compressed_imgmsg(self.frame[-1]))

    def update_camera(self):
        frame = None
        while True:
            if self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    scale_percent = 80  # percent of original size
                    if scale_percent != 100:
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
