#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import math

class DronePosePublisher(Node):
    def __init__(self):
        super().__init__('drone_pose_publisher')

        # Subscribe to the PX4 visualizer pose topic
        self.sub_pose = self.create_subscription(
            PoseStamped,
            '/px4_visualizer/vehicle_pose',
            self.pose_callback,
            10
        )

        # Optional: republish under a simpler topic if other nodes expect /drone/pose
        self.pub_pose = self.create_publisher(PoseStamped, '/drone/pose', 10)

        self.drone_pos = None  # numpy array for convenience
        self.trueYaw = 0.0     # Yaw in radians

        self.get_logger().info("Subscribed to /px4_visualizer/vehicle_pose")

    def pose_callback(self, msg: PoseStamped):
        # Store position as list
        self.drone_pos = [
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z
        ]

        # Compute true yaw from quaternion
        q = msg.pose.orientation
        self.trueYaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )

        # Republish pose if needed
        self.pub_pose.publish(msg)

        self.get_logger().debug(
            f"Drone pose: x={msg.pose.position.x:.2f}, "
            f"y={msg.pose.position.y:.2f}, z={msg.pose.position.z:.2f}, "
            f"yaw={math.degrees(self.trueYaw):.2f} deg"
        )

def main(args=None):
    rclpy.init(args=args)
    node = DronePosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()