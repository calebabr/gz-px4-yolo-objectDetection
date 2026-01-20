from cProfile import label
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import torch
from torchvision import transforms
from image_processing.forest_model import ForestCNN
from PIL import Image as PILImage
import torch.nn.functional as F

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

        # Load model
        self.model = ForestCNN(num_classes=2)
        self.model.load_state_dict(torch.load('/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/2class.pth', map_location='cpu')) # add model path
        self.model.eval()
 
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])

    def listener_callback(self, msg):
        # Convert ROS image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Preprocess
        img_pil = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img_tensor = self.transform(PILImage.fromarray(img_pil)).unsqueeze(0)

        # Inference
        with torch.no_grad():
            outputs = self.model(img_tensor)  # raw logits

            # Apply softmax to get probabilities
            probs = F.softmax(outputs, dim=1)

            # Get max probability and predicted class index
            max_prob, predicted = torch.max(probs, 1)

        CLASS_NAMES = ['forest', 'no_forest']
        max_prob_value = max_prob.item()
        predicted_idx = predicted.item()

        threshold = 0.6  # example threshold; tune this for your use case
        if max_prob_value < threshold:
            label = "uncertain"
        else:
            label = CLASS_NAMES[predicted_idx]

        self.get_logger().info(f'Prediction: {label} (confidence: {max_prob_value:.2f})')


def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
