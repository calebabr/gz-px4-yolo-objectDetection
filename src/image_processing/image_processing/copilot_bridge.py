import json
import os
import threading

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

from image_processing import copilot_logic as logic
from image_processing_msgs.msg import DetectionArray


class CopilotBridge(Node):
    """Answers player questions from Unity using the latest game state, detections and camera frame.

    /copilot/question (String, JSON {"id", "text", "persona"})  ->  /copilot/answer (String, JSON {"id", "text", "source"})
    The OpenAI key is read from an environment variable on the ROS machine and is never logged or published.
    """

    def __init__(self):
        super().__init__('copilot_bridge')
        self.declare_parameter('mock', False)
        self.declare_parameter('model', logic.DEFAULT_MODEL)
        self.declare_parameter('api_key_env', 'OPENAI_API_KEY')
        self.declare_parameter('timeout_s', 20.0)
        self.declare_parameter('include_image', True)

        self.state = {}
        self.detections = []
        self.image_jpeg = None
        self.lock = threading.Lock()

        self.create_subscription(String, '/game/state', self.on_state, 10)
        self.create_subscription(DetectionArray, '/yolo/detections', self.on_detections, 10)
        self.create_subscription(CompressedImage, '/camera/image_raw/compressed', self.on_image, 1)
        self.create_subscription(String, '/copilot/question', self.on_question, 10)
        self.answer_pub = self.create_publisher(String, '/copilot/answer', 10)

        mode = 'MOCK' if self.get_parameter('mock').value else 'OpenAI (%s)' % self.get_parameter('model').value
        self.get_logger().info('Copilot bridge ready, mode: %s' % mode)

    def on_state(self, msg):
        try:
            state = json.loads(msg.data)
        except ValueError:
            return
        with self.lock:
            self.state = state

    def on_detections(self, msg):
        detections = [{'class_name': d.class_name, 'confidence': d.confidence} for d in msg.detections]
        with self.lock:
            self.detections = detections

    def on_image(self, msg):
        with self.lock:
            self.image_jpeg = bytes(msg.data)

    def on_question(self, msg):
        try:
            request = json.loads(msg.data)
            question = str(request['text'])
        except (ValueError, KeyError, TypeError):
            self.get_logger().warn('Ignoring malformed /copilot/question')
            return
        threading.Thread(target=self.answer, args=(request.get('id', ''), question, request.get('persona', 'default'), request.get('detail', 'standard')),
                         daemon=True).start()

    def answer(self, request_id, question, persona, detail='standard'):
        with self.lock:
            state = dict(self.state)
            detections = list(self.detections)
            image = self.image_jpeg if self.get_parameter('include_image').value else None

        api_key = os.environ.get(self.get_parameter('api_key_env').value, '')
        text, source = logic.answer_question(
            question, persona, state, detections, image, api_key,
            self.get_parameter('model').value,
            mock=self.get_parameter('mock').value,
            timeout=float(self.get_parameter('timeout_s').value),
            detail=detail)

        self.answer_pub.publish(String(data=json.dumps({'id': request_id, 'text': text, 'source': source})))
        self.get_logger().info('Answered question %s via %s' % (request_id, source))


def main(args=None):
    rclpy.init(args=args)
    node = CopilotBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
