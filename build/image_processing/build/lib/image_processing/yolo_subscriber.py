import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
import torch
import numpy as np

from std_msgs.msg import String

from image_processing_msgs.msg import Detection, DetectionArray

class YoloSubscriber(Node):
    def __init__(self):
        super().__init__('yolo_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        self.bridge = CvBridge()
        self.image_pub = self.create_publisher(Image, '/yolo/image_annotated', 10)  # Camera View Topic
        # self.detection_pub = self.create_publisher(String, '/yolo/detections', 10)  # String Topic to Communicate to QGC
        self.detection_pub = self.create_publisher(DetectionArray, '/yolo/detections', 10) # Detection

        # Update path here depending on model being used
        self.model = YOLO('/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/YOLOv8/best.pt')  
        # self.model = YOLO('/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/YOLOv11_1.0/yolo11n.pt')
        # self.model = YOLO('/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/yolo_model_export/content/runs/detect/train/weights/best.pt')  

        self.get_logger().info("YOLO model loaded.")

    def listener_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            results = self.model(cv_image)

            boxes = results[0].boxes
            detected_classes = [self.model.names[int(cls_id)] for cls_id in boxes.cls]

            # Draw bounding boxes
            annotated_frame = results[0].plot()

            ros_image = self.bridge.cv2_to_imgmsg(annotated_frame, encoding='bgr8')
            self.image_pub.publish(ros_image)

            # Prepare detection string to /yolo/detections
            # if detected_classes:
                # detected_str = ','.join(detected_classes)
                # self.detection_pub.publish(String(data=detected_str))  # <-- Publish detections
                # self.get_logger().info(f'Detected: {detected_str}')

            # Publish Array 
            detection_array = DetectionArray()
            for box in results[0].boxes:
                det = Detection()
                det.class_name = self.model.names[int(box.cls)]
                det.confidence = float(box.conf)
                det.x_min, det.y_min, det.x_max, det.y_max = map(float, box.xyxy[0])
                det.width = (det.x_max -  det.x_min)
                det.height = (det.y_max -  det.y_min)
                det.pixel_area  = (det.height * det.width)
                det.x_center = (det.x_max + det.x_min) * np.float32(0.5)
                det.y_center = (det.y_max + det.y_min) * np.float32(0.5)
                detection_array.detections.append(det)

            self.detection_pub.publish(detection_array)
        except Exception as e:
            self.get_logger().error(f"Error: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = YoloSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()