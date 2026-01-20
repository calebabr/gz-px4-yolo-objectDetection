import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import time
import threading
import sys
import tty
import termios
import re

class ImageLabeler(Node):
    def __init__(self):
        super().__init__('image_labeler')
        self.bridge = CvBridge()
        self.latest_image = None

        # Define labels and key bindings
        self.labels = {
            'c': 'car',
            'p': 'person',
            'b': 'building',
            't': 'tree'
        }

        self.data_dir = '/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/data'
        self.label_dirs = {}
        self.label_indices = {}

        for key, label in self.labels.items():
            label_dir = os.path.join(self.data_dir, label)
            os.makedirs(label_dir, exist_ok=True)
            self.label_dirs[label] = label_dir
            self.label_indices[label] = self.get_next_index(label_dir, label)

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        threading.Thread(target=self.keyboard_listener, daemon=True).start()
        self.get_logger().info('Controls:')
        for key, label in self.labels.items():
            self.get_logger().info(f'  Press "{key}" to save {label} image.')

    def get_next_index(self, directory, prefix):
        existing_files = os.listdir(directory)
        pattern = re.compile(rf"{prefix}_(\d+)\.jpg")
        max_index = 0
        for fname in existing_files:
            match = pattern.match(fname)
            if match:
                idx = int(match.group(1))
                max_index = max(max_index, idx)
        return max_index + 1

    def image_callback(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"Image conversion failed: {e}")

    def save_image(self, label):
        if self.latest_image is None:
            self.get_logger().warn('No image received yet.')
            return

        filename = f'{label}_{self.label_indices[label]:03d}.jpg'
        path = os.path.join(self.label_dirs[label], filename)
        self.label_indices[label] += 1

        cv2.imwrite(path, self.latest_image)
        self.get_logger().info(f'Saved {label} image to: {path}')

    def keyboard_listener(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        try:
            while True:
                key = sys.stdin.read(1)
                if key in self.labels:
                    self.save_image(self.labels[key])
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main(args=None):
    rclpy.init(args=args)
    node = ImageLabeler()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()