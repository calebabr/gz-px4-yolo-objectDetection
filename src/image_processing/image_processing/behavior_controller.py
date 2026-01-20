#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from collections import deque
from std_msgs.msg import String
from image_processing_msgs.msg import DetectionArray
from image_processing_msgs.msg import Detection
from image_processing_msgs.msg import ProminentObject, ProminentObjectArray
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import PoseStamped
import numpy as np
import csv
import os
from datetime import datetime
import itertools

from sensor_msgs.msg import Image



def image_callback(self, msg: Image):
    self.image_width = msg.width
    self.image_height = msg.height

class BehaviorController(Node):
    def __init__(self):
        super().__init__('behavior_controller')

        # Subscriptions
        self.sub_yolo = self.create_subscription(
            DetectionArray, '/yolo/detections', self.callback, 10)
        self.sub_pose = self.create_subscription(
            PoseStamped, '/drone/pose', self.pose_callback, 10)
        self.pub_prominent = self.create_publisher(Detection, '/yolo/prominent', 10)
        self.pub_features = self.create_publisher(Float32MultiArray, '/yolo/features', 10)
        self.pub_prominent_custom = self.create_publisher(ProminentObject, '/behavior/prominent_object', 10)
        self.pub_prominent_array = self.create_publisher(ProminentObjectArray, '/behavior/prominent_array', 10)
        self.sub_image = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.image_width = None
        self.image_height = None

        self.drone_pos = np.array([0.0, 0.0, 0.0])
        self.history = deque(maxlen=5)

        self.frame_count = 0  
        self.log_every_n_frames = 5  # Adjust to 5–10 

        # Parameters
        self.declare_parameter('sigmoid_k', 5.0)
        self.declare_parameter('sigmoid_x0', 0.5)
        self.declare_parameter('conf_weight', 0.7)
        self.declare_parameter('area_weight', 0.3)
        
        # k = [5, 10, 15, 20]
        # x0 = [0.5, 0.67, 0.75]
        # conf_weight = (0.7, 0.6, 0.5, 0.4)
        # area_weight = (0.3, 0.4, 0.5, 0.6)

        # Define parameter search space
        k_values = [5.0, 10.0, 15.0, 20.0]
        x0_values = [0.5, 0.67, 0.75]
        conf_weights = [0.7, 0.6, 0.5, 0.4, 0.3]
        area_weights = [0.3, 0.4, 0.5, 0.6, 0.7]

        conf_area_pairs = list(zip(conf_weights, area_weights))  

        self.param_grid = [(k, x0, conf, area) 
                   for k in k_values 
                   for x0 in x0_values 
                   for conf, area in zip(conf_weights, area_weights)]        
        self.current_param_idx = 0
        # self.set_current_params()

        # Object positions (from baylands_noTrees.sdf)
        self.objects = {
            "casual_female": {
                "class": "person",
                "position": np.array([-10.618467534215167, -7.4531963026138293,  0])
            },
        }

        # CSV
        # self.csv_file = "ImprovedDistanceEstimatorData.csv"
        # csv_dir = os.path.dirname(self.csv_file)

        # if csv_dir != "":
        #     os.makedirs(csv_dir, exist_ok=True)

        # file_exists = os.path.isfile(self.csv_file)
        # with open(self.csv_file, "a", newline="") as f:
        #     writer = csv.writer(f)
        #     if not file_exists:
        #         writer.writerow([
        #             "pred_conf", "pred_area","score", "width", "height", "aspect_ratio",
        #             "distance_x", "distance_y", "distance_z"
        #         ])
    
    def to_prominent_object_msg(self, det: Detection, score: float):
        msg = ProminentObject()
        msg.class_name = det.class_name
        msg.x_center = det.x_center
        msg.y_center = det.y_center
        msg.size_score = float(score)
        return msg

    def image_callback(self, msg: Image):
        self.image_width = msg.width
        self.image_height = msg.height

    def sigmoid(self, x, k, x0):
        return 1 / (1 + np.exp(-k * (x - x0)))

    def pose_callback(self, msg: PoseStamped):
        self.drone_pos = np.array([
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z
        ])
        # self.get_logger().debug(f"Drone pos updated: {self.drone_pos}")

    def compute_correct_prominent(self):
        min_dist = float('inf')
        closest_name, closest_class = None, None
        for name, info in self.objects.items():
            dist = np.linalg.norm(self.drone_pos - info["position"])
            if dist < min_dist:
                min_dist = dist
                closest_name = name
                closest_class = info["class"]
        return closest_name, min_dist, closest_class

    def set_current_params(self):
        k, x0, conf_weight, area_weight = self.param_grid[self.current_param_idx]
        self.k, self.x0 = k, x0
        self.conf_weight, self.area_weight = conf_weight, area_weight
        self.get_logger().info(f"Now testing params: k={k}, x0={x0}, conf_weight={conf_weight}, area_weight={area_weight}")

    def next_params(self):
        if self.current_param_idx + 1 < len(self.param_grid):
            self.current_param_idx += 1
            self.set_current_params()
        else:
            self.get_logger().info("Finished all parameter combinations.")
            rclpy.shutdown()
    
    def callback(self, msg: DetectionArray):
        self.frame_count += 1
        if self.frame_count % self.log_every_n_frames != 0:
            return  # Only going to log every 1 to n frames
        
        if not msg.detections:
            self.get_logger().warn("No detections received.")
            return
        
        k, x0, conf_weight, area_weight = 15, 0.5, 0.6, 0.4

        # conf_weight = self.get_parameter('conf_weight').get_parameter_value().double_value
        # area_weight = self.get_parameter('area_weight').get_parameter_value().double_value
        # k = self.get_parameter('sigmoid_k').get_parameter_value().double_value
        # x0 = self.get_parameter('sigmoid_x0').get_parameter_value().double_value

        feature_list = []

        areas, confs, class_names, valid_dets = [], [], [], []
        for det in msg.detections:
            if not getattr(det, "class_name", None):
                continue
            if det.confidence <= 0.0 or det.pixel_area <= 0.0:
                continue
            areas.append(det.pixel_area)
            confs.append(det.confidence)
            class_names.append(det.class_name)
            valid_dets.append(det)

        if not valid_dets:
            return

        areas = np.array(areas, dtype=np.float32)
        confs = np.array(confs, dtype=np.float32)
        max_area = np.max(areas) if areas.size > 0 else 1.0

        best_idx, best_score = None, -np.inf
        for i, (area, conf) in enumerate(zip(areas, confs)):
            norm_area = area / (max_area + 1e-6)
            norm_conf = conf
            w_conf = self.sigmoid(norm_conf, k, x0)
            score = conf_weight * w_conf + area_weight * norm_area
            if score > best_score:
                best_score = score
                best_idx = i

        main = valid_dets[best_idx]
        self.history.append(main)
        # prominent = max(set(self.history), key=self.history.count)

        matching_objs = [obj for obj in self.objects.values() if obj["class"] == main.class_name]
        if matching_objs:
            obj = matching_objs[0]
            distance_x = np.linalg.norm(self.drone_pos[0] - obj["position"][0])
            distance_y = np.linalg.norm(self.drone_pos[1] - obj["position"][1])
            distance_z = abs(self.drone_pos[2] - obj["position"][2])    
        else:
            distance_x = distance_y = distance_z =None

        correct_name, correct_dist, correct_class = self.compute_correct_prominent()
        label = 0 if main.class_name == correct_class else 1

        classes = [det.class_name for det in self.history]
        most_freq_class = max(set(classes), key=classes.count)
        prominent = next(det for det in reversed(self.history) if det.class_name == most_freq_class)

        self.pub_prominent.publish(prominent)

        # Publish single prominent object in new custom format
        prominent_msg = self.to_prominent_object_msg(main, best_score)
        self.pub_prominent_custom.publish(prominent_msg)

        # Publish array of all detections in custom format
        array_msg = ProminentObjectArray()
        for det, area, conf in zip(valid_dets, areas, confs):
            # recompute score for each detection
            norm_area = det.pixel_area / (max_area + 1e-6)
            w_conf = self.sigmoid(det.confidence, k, x0)
            sc = conf_weight * w_conf + area_weight * norm_area

            array_msg.objects.append(self.to_prominent_object_msg(det, sc))

        self.pub_prominent_array.publish(array_msg)
        
        # # Append row with current params
        # timestamp = datetime.now().isoformat()
        #distance_xyz = np.linalg.norm(self.drone_pos - self.objects[0]["position"])
        #distance_xy = np.linalg.norm(self.drone_pos[:2] - self.objects[0]["position"][:2])
        
        bbox_width = main.width
        bbox_height = main.height
        bbox_aspect_ratio = bbox_width / bbox_height if bbox_height > 0 else 0

        center_x = main.x_center
        center_y = main.y_center
        center_x_diff = (center_x - (self.image_width / 2))
        center_y_diff = center_y - (self.image_height / 2)
        center_x_diff_norm = center_x_diff / (self.image_width / 2)
        center_y_diff_norm = center_y_diff / (self.image_height / 2)

        # with open(self.csv_file, "a", newline="") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([
        #         main.confidence,
        #         main.pixel_area,
        #         best_score,
        #         bbox_width,
        #         bbox_height,
        #         bbox_aspect_ratio,
        #         distance_x if distance_x is not None else "N/A",
        #         distance_y if distance_y is not None else "N/A",
        #         distance_z if distance_z is  not None else "N/A",
        #     ])

        # # After N frames for one param set, switch to next
        # if self.frame_count > 900:  # e.g. 150 frames per param set
        #     self.frame_count = 0
        #     self.next_params()
        
        # Append features in order used by distance predictor
        features = [
            det.confidence,
            det.pixel_area,
            score,
            bbox_width,
            bbox_height,
            bbox_aspect_ratio,
        ]
        feature_list.extend(features)  # flatten into a single list for Float32MultiArray

        # Publish as Float32MultiArray
        if feature_list:
            out_msg = Float32MultiArray(data=feature_list)
            self.pub_features.publish(out_msg)
            self.get_logger().info(f"Published features for {len(msg.detections)} detections")

        self.get_logger().info(
            f"Chosen: {main.class_name} (area={main.pixel_area:.1f}, conf={main.confidence:.2f}, score={best_score:.2f}) "
            f"smoothed: {prominent}, label: {label}, distance: {distance_x}, correct_class_name: {correct_class}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = BehaviorController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()