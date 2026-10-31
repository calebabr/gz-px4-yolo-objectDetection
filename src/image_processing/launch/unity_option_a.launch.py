import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    default_model = os.path.expanduser(
        '~/ros2_px4_offboard_example_ws/src/image_processing/YOLOv8/best.pt')

    return LaunchDescription([
        DeclareLaunchArgument('model_path', default_value=default_model,
                              description='Path to the YOLO weights (.pt/.onnx)'),
        DeclareLaunchArgument('ros_ip', default_value='0.0.0.0'),
        DeclareLaunchArgument('ros_tcp_port', default_value='10000'),

        # Unity <-> ROS bridge (ROS-TCP-Endpoint)
        Node(
            package='ros_tcp_endpoint',
            executable='default_server_endpoint',
            name='unity_endpoint',
            parameters=[{
                'ROS_IP': LaunchConfiguration('ros_ip'),
                'ROS_TCP_PORT': LaunchConfiguration('ros_tcp_port'),
            }],
            output='screen',
        ),

        # Unity publishes JPEG on /camera/image_raw/compressed; YOLO wants raw Image
        Node(
            package='image_transport',
            executable='republish',
            name='unity_image_republish',
            arguments=['compressed', 'raw'],
            remappings=[
                ('in/compressed', '/camera/image_raw/compressed'),
                ('out', '/camera/image_raw'),
            ],
            output='screen',
        ),

        Node(
            package='image_processing',
            executable='yolo_subscriber',
            name='yolo_subscriber',
            parameters=[{'model_path': LaunchConfiguration('model_path')}],
            output='screen',
        ),

        Node(
            package='image_processing',
            executable='behavior_controller',
            name='behavior_controller',
            output='screen',
        ),
    ])
