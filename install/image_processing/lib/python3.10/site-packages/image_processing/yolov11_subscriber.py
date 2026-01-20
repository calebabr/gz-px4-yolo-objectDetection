import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
import onnxruntime as ort
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

# QoS for image_raw
qos_profile = QoSProfile(depth=10)
qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT

class Yolov11Subscriber(Node):
    def __init__(self):
        super().__init__('yolov11_subscriber')
        
        # ROS2 subscription/publisher
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            qos_profile
        )
        self.image_pub = self.create_publisher(Image, '/yolo/image_annotated', 10)

        # Load ONNX model and class names
        model_path = '/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/yolo_model_export/content/runs/detect/train/weights/best.onnx'
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name

        class_path = '/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/yolo_model_export/class_names.txt'
        with open(class_path, 'r') as f:
            self.class_names = [line.strip() for line in f]

        self.get_logger().info('✅ YOLOv11 ONNX model loaded.')

    def preprocess(self, image):
        # Resize with aspect ratio and pad to 640x640 (letterboxing)
        input_size = 640
        h, w = image.shape[:2]
        scale = min(input_size / w, input_size / h)
        nw, nh = int(scale * w), int(scale * h)

        resized_image = cv2.resize(image, (nw, nh))
        padded_image = np.full((input_size, input_size, 3), 114, dtype=np.uint8)
        padded_image[0:nh, 0:nw] = resized_image

        # Convert to RGB and normalize
        img = cv2.cvtColor(padded_image, cv2.COLOR_BGR2RGB).astype(np.float32)
        img /= 255.0
        img = np.transpose(img, (2, 0, 1))  # HWC to CHW
        img = np.expand_dims(img, axis=0)  # Add batch dim
        return img.astype(np.float32), scale, nw, nh


    def postprocess(self, predictions, scale, nw, nh, orig_shape, conf_thresh=0.4, iou_thresh=0.45):
        h_orig, w_orig = orig_shape
        detections = []

        if predictions[0].ndim != 2:
            self.get_logger().warn("Unexpected prediction shape")
            return detections

        for pred in predictions[0]:
            if len(pred) < 6:
                continue

            x_center, y_center, width, height, conf, *class_scores = pred
            score = conf * max(class_scores)
            if score < conf_thresh:
                continue

            class_id = int(np.argmax(class_scores))

            # Convert to x1,y1,x2,y2 in original image space
            x1 = (x_center - width / 2) * (w_orig / nw)
            y1 = (y_center - height / 2) * (h_orig / nh)
            x2 = (x_center + width / 2) * (w_orig / nw)
            y2 = (y_center + height / 2) * (h_orig / nh)

            detections.append((int(x1), int(y1), int(x2), int(y2), class_id, score))

        return detections


    def listener_callback(self, msg):
        try:
            self.get_logger().info("Image received")
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            input_tensor, scale, nw, nh = self.preprocess(frame)

            # ONNX inference
            outputs = self.session.run(None, {self.input_name: input_tensor})
            detections = self.postprocess(outputs, scale, nw, nh, frame.shape[:2])

            self.get_logger().info(f"Detections: {len(detections)}")

            for x1, y1, x2, y2, class_id, score in detections:
                label = f"{self.class_names[class_id]}: {score:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                self.get_logger().info(f"Detected: {label}")

            # Publish the annotated image
            annotated_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            annotated_msg.header = msg.header  # preserve header
            self.image_pub.publish(annotated_msg)
            self.get_logger().info("Published annotated image")

        except Exception as e:
            self.get_logger().error(f"Error during inference: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = Yolov11Subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()