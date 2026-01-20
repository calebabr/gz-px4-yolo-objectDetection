import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/cjabrantes/ros2_px4_offboard_example_ws/install/px4_offboard'
