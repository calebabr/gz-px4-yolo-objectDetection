#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from px4_msgs.msg import TrajectorySetpoint
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray
import numpy as np

class PIDController:
    """Simple PID controller."""
    def __init__(self, kp, ki=0.0, kd=0.0, dt=0.05, output_limits=(-1.0, 1.0)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.output_limits = output_limits
        self.integral = 0.0
        self.prev_error = 0.0

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, error):
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return float(np.clip(output, self.output_limits[0], self.output_limits[1]))

class Velocity:
    """Simple container for FLU velocity."""
    def __init__(self):
        self.x = 0.0  # FLU forward/back
        self.y = 0.0  # FLU left/right
        self.z = 0.0  # FLU up/down

class DroneBehaviorNode(Node):
    def __init__(self):
        super().__init__('drone_behavior_node')

        # Subscriptions
        self.sub_pose = self.create_subscription(PoseStamped, '/drone/pose', self.pose_callback, 10)
        self.sub_distances = self.create_subscription(Float32MultiArray, '/object_distance_xyz', self.distance_callback, 10)
        self.sub_features = self.create_subscription(
            Float32MultiArray,
            '/yolo/features',
            self.feature_callback,
            10
        )

        self.center_x_norm = 0.0
        self.center_y_norm = 0.0

        # Publisher
        self.pub_setpoint = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)

        # Drone state
        self.current_pos = np.array([0.0, 0.0, 0.0])
        self.target_distance = None       # object_pos - drone_pos
        self.center_diff_norm = np.array([0.0, 0.0])

        # Velocity and yaw
        self.velocity = Velocity()
        self.trueYaw = 0.0
        self.pid_yaw = PIDController(kp=100.0, dt=0.05, output_limits=(-1.0, 1.0))

        # PID controllers for X/Y/Z
        # Increased gains and output limits for more responsiveness
        self.pid_x = PIDController(kp=0.50, ki=0.0, kd=0.12, dt=0.05, output_limits=(-5.0, 5.0))
        self.pid_y = PIDController(kp=0.50, ki=0.0, kd=0.12, dt=0.05, output_limits=(-5.0, 5.0))
        self.pid_z = PIDController(kp=0.05, ki=0.0, kd=0.75, dt=0.05, output_limits=(-1.5, 1.5))
        # self.pid_z = PIDController(kp=0, ki = 0, kd = 0, dt=0.05)
        self.k_yaw = 0.75   

        # Timer
        self.timer = self.create_timer(0.05, self.timer_callback)

        self.get_logger().info("DroneBehaviorNode with PID + yaw control started")
        # small multiplier applied to final velocity setpoints for more aggressive motion
        self.velocity_scale = 1.2
        # Runtime parameter to choose whether to rotate world velocities into vehicle/body frame
        # Set to True to keep previous behavior (rotate by yaw). Set to False to publish world/NED velocities directly.
        self.declare_parameter('rotate_to_body_frame', False)
        self.rotate_to_body = bool(self.get_parameter('rotate_to_body_frame').value)
        # Rotation sign parameter: use 1 to rotate by +yaw, -1 to rotate by -yaw (default -1 matches R(-yaw)).
        self.declare_parameter('rotate_yaw_sign', -1)
        self.rotate_yaw_sign = int(self.get_parameter('rotate_yaw_sign').value)

    def pose_callback(self, msg: PoseStamped):
        self.current_pos = np.array([
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z
        ])
        # compute yaw from quaternion so rotations are correct
        q = msg.pose.orientation
        # yaw (around Z) from quaternion
        self.trueYaw = np.arctan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )

    def distance_callback(self, msg: Float32MultiArray):
        data = msg.data
        if len(data) < 3:
            self.get_logger().warn("Received empty distance array.")
            return
        # low-pass filter target distance to reduce sensor/model jitter
        new_dist = np.array(data[0:3], dtype=np.float32)
        if self.target_distance is None:
            self.target_distance = new_dist
        else:
            # Make filtering more responsive (higher alpha favors new measurement)
            alpha = 0.9
            self.target_distance = alpha * new_dist + (1.0 - alpha) * self.target_distance
        if len(data) >= 5:
            self.center_diff_norm = np.array(data[3:5], dtype=np.float32)
    
    def feature_callback(self, msg: Float32MultiArray):
        data = msg.data
        if len(data) < 8:
            return

        self.center_x_norm = float(data[6])  
        self.center_y_norm = float(data[7])  

    def timer_callback(self):
        setpoint = TrajectorySetpoint()
        vx, vy, vz = 0.0, 0.0, 0.0
        yaw_speed = 0.0

        if self.target_distance is not None:
            # target_distance = object_pos - drone_pos (positive means object is in that direction)
            # Desired offset from object in world frame (object-relative position where the drone should stop)
            desired_offset = np.array([2.0, 2.0, -3.0], dtype=np.float32)

            # Compute error relative to desired offset
            dist_error = self.target_distance - desired_offset

            # small deadband to avoid chasing tiny errors / oscillation
            deadband = 0.05
            dist_error = np.where(np.abs(dist_error) < deadband, 0.0, dist_error)

            # PID outputs for world frame (X, Y, Z)
            pid_x_world = self.pid_x.compute(dist_error[0])
            pid_y_world = self.pid_y.compute(dist_error[1])
            pid_z_world = self.pid_z.compute(dist_error[2])

            # Directly use PID outputs as world velocities
            vx_world = pid_x_world
            vy_world = pid_y_world
            vz_world = pid_z_world

            # Debug: print pose/distance/yaw to help verify sign/frame conventions
            yaw_deg = np.degrees(self.trueYaw)
            try:
                td = np.array(self.target_distance)
            except Exception:
                td = self.target_distance

            self.get_logger().info(
                f"pos=({self.current_pos[0]:+.2f},{self.current_pos[1]:+.2f},{self.current_pos[2]:+.2f}) | "
                f"target=({td[0]:+.2f},{td[1]:+.2f},{td[2]:+.2f}) | "
                f"desired=({desired_offset[0]:+.2f},{desired_offset[1]:+.2f},{desired_offset[2]:+.2f}) | "
                f"yaw={yaw_deg:+.1f}deg"
            )

            # Convert world frame → the frame we publish in (toggleable)
            # If rotate_to_body is True, rotate world velocities into the vehicle/body frame using -yaw.
            # If False, publish world frame velocities directly (only flip Z to NED convention).
            cos_yaw = np.cos(self.trueYaw)
            sin_yaw = np.sin(self.trueYaw)

            if self.rotate_to_body:
                # Rotate world -> body by angle = rotate_yaw_sign * yaw.
                # Use rotation_sign either -1 (R(-yaw)) or +1 (R(+yaw)).
                rotation_sign = -1 if self.rotate_yaw_sign < 0 else 1
                vx_out = vx_world * cos_yaw - vy_world * (rotation_sign * sin_yaw)
                vy_out = vx_world * (rotation_sign * sin_yaw) + vy_world * cos_yaw
            else:
                # Publish in world frame (assumed ENU -> convert to NED by swapping/negating Z only)
                vx_out = vx_world
                vy_out = vy_world

            vz_out = -vz_world  # Z up -> Z down for PX4 (NED)

            vx, vy, vz = vx_out, vy_out, vz_out

            # steering for yaw from normalized center offset
            yaw_speed = float(self.k_yaw * self.center_x_norm)

            # clamp for safety
            yaw_speed = float(max(min(yaw_speed, 7.5), -7.5))

            self.get_logger().info(
                f"dist_error=({dist_error[0]:+.2f},{dist_error[1]:+.2f},{dist_error[2]:+.2f}) | "
                f"world_vel=({vx_world:+.2f},{vy_world:+.2f},{vz_world:+.2f}) | "
                f"out_vel=({vx:+.2f},{vy:+.2f},{vz:+.2f}) | yaw_speed={yaw_speed:+.2f} | "
                f"rotate_to_body={self.rotate_to_body}"
            )

        # Publish velocity setpoint (apply small global scale)
        setpoint.position = [float('nan')] * 3
        setpoint.velocity = [vx * self.velocity_scale, vy * self.velocity_scale, vz * self.velocity_scale]
        setpoint.acceleration = [float('nan')] * 3
        setpoint.jerk = [float('nan')] * 3
        setpoint.yaw = float('nan')
        setpoint.yawspeed = yaw_speed

        self.pub_setpoint.publish(setpoint)

def main(args=None):
    rclpy.init(args=args)
    node = DroneBehaviorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()