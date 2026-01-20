#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import PoseStamped
import numpy as np


class DistancePublisher(Node):
    """Simple node that publishes absolute vector distance from the drone
    to a known object position.

    This restores the original behavior: subscribe to `/drone/pose`, compute
    object_pos - drone_pos and publish as a `Float32MultiArray` on
    `/object_distance_xyz`.
    """

    def __init__(self):
        super().__init__('distance_publisher')

        # Subscribe to the drone pose
        self.sub_pose = self.create_subscription(
            PoseStamped,
            '/drone/pose',
            self.pose_callback,
            10
        )

        # Publisher for the distance to the casual female
        self.pub_distances = self.create_publisher(
            Float32MultiArray,
            '/object_distance_xyz',
            10
        )

        # Position of the casual female in world frame (known a priori)
        self.casual_female_pos = np.array([-10.0, -7.0, 0.0])

        # Store drone position
        self.drone_pos = None

        self.get_logger().info("DistancePublisher to casual female started.")

    def pose_callback(self, msg: PoseStamped):
        # Store drone position
        self.drone_pos = np.array([
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z
        ])

        if self.drone_pos is None:
            return

        # Compute relative distance: drone - object (positive means toward object when negative)
        # We invert so that positive error naturally drives toward the object
        diff = self.drone_pos - self.casual_female_pos

        # Publish as Float32MultiArray
        out_msg = Float32MultiArray(data=diff.tolist())
        self.pub_distances.publish(out_msg)

        # Logging
        self.get_logger().info(
            f"Distance to casual female: dx={diff[0]:.2f}, dy={diff[1]:.2f}, dz={diff[2]:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = DistancePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


# -----------------------------------------------------------------------------
# NOTE: ML-based predictor code (kept here for reference) ---------------------
# If you want to use the trained model again, the code below shows how it was
# structured. The model file is located at:
#   src/image_processing/distance_model_light.pkl
#
# Example (commented):
#
# import joblib
# from image_processing_msgs.msg import DetectionArray, ProminentObject
#
# model_path = '/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/distance_model_light.pkl'
# model = joblib.load(model_path)
#
# # Subscribe to detections/prominent, build feature vector in the same order
# # as `behavior_controller` published features and call `model.predict()`.
# # The rest of the code above publishes the ML prediction to
# # `/object_distance_xyz` as Float32MultiArray([dx, dy, dz]).
# -----------------------------------------------------------------------------
