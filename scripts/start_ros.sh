#!/usr/bin/env bash
# One-command ROS side for the Unity option-A setup (run inside WSL Ubuntu-22.04).
# Usage: scripts/start_ros.sh [model_path] [launch args...]      e.g.  scripts/start_ros.sh copilot_mock:=true
#   model_path    optional path to the YOLO weights (a first argument without ':=' is taken as the model path)
#   copilot_mock:=true   canned copilot answers, no OpenAI call
# The copilot reads its key from the OPENAI_API_KEY environment variable (never from a file in the repo).
set -e
source /opt/ros/humble/setup.bash
source ~/unity_ws/install/setup.bash
source ~/ros2_px4_offboard_example_ws/install/setup.bash

ARGS=()
if [ -n "$1" ] && [[ "$1" != *":="* ]]; then ARGS+=("model_path:=$1"); shift; fi
exec ros2 launch image_processing unity_option_a.launch.py "${ARGS[@]}" "$@"
