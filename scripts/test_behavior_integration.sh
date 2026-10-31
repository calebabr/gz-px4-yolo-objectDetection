#!/usr/bin/env bash
# Integration test for behavior_controller over real ROS topics (run inside WSL after colcon build).
# R-3: /yolo/features must describe the CHOSEN detection (not the last one in the list).
# R-4: by default every detection frame is processed (not 1 in 5), and the rate is a parameter.
# R-3b: it must not crash before the first image arrives (image size unknown).
source /opt/ros/humble/setup.bash
source ~/unity_ws/install/setup.bash
source ~/ros2_px4_offboard_example_ws/install/setup.bash

FAILED=0
PIDS=()
cleanup() { for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null; done; pkill -f "image_processing/behavior_controller" 2>/dev/null; }
trap cleanup EXIT

# best detection (conf .95, area 2000) first, a weaker one last
DETECTIONS="{detections: [{class_name: person, confidence: 0.95, pixel_area: 2000.0, width: 40.0, height: 50.0, x_center: 320.0, y_center: 240.0}, {class_name: person, confidence: 0.30, pixel_area: 100.0, width: 10.0, height: 10.0, x_center: 100.0, y_center: 100.0}]}"

run_node() {  # extra ros args
    ros2 run image_processing behavior_controller --ros-args "$@" > /tmp/behavior_test.log 2>&1 &
    NODE=$!; PIDS+=("$NODE")
    sleep 3
}
# `ros2 run` leaves its child node alive when the wrapper is killed, so stop the node itself
stop_node() { kill "$NODE" 2>/dev/null; pkill -f "image_processing/behavior_controller" 2>/dev/null; wait "$NODE" 2>/dev/null; sleep 1; }

# --- R-3 (+ no crash without an image) ---
run_node
OUT=$(mktemp)
timeout 12 ros2 topic echo --once /yolo/features std_msgs/msg/Float32MultiArray > "$OUT" 2>/dev/null &
ECHO=$!
sleep 1
ros2 topic pub -r 5 /yolo/detections image_processing_msgs/msg/DetectionArray "$DETECTIONS" > /dev/null 2>&1 &
PUB=$!; PIDS+=("$PUB")
wait "$ECHO"
kill "$PUB" 2>/dev/null

# data: [confidence, pixel_area, score, width, height, aspect]
FIRST=$(grep -A1 "^data:" "$OUT" | tail -1 | tr -d ' -')
SECOND=$(grep -A2 "^data:" "$OUT" | tail -1 | tr -d ' -')
if [[ "$FIRST" == 0.9* ]] && [[ "$SECOND" == 2000* ]]; then
    echo "PASS  R-3 features describe the chosen detection (conf $FIRST, area $SECOND)"
else
    echo "FAIL  R-3 features: conf='$FIRST' area='$SECOND' (expected 0.95 / 2000)"; cat "$OUT"; FAILED=1
fi
if grep -q "TypeError" /tmp/behavior_test.log; then
    echo "FAIL  node raised a TypeError before the first image"; FAILED=1
else
    echo "PASS  no crash while the image size is still unknown"
fi
rm -f "$OUT"; stop_node

# --- R-4: default processes every frame ---
run_node
COUNT_OUT=$(mktemp)
(timeout 4 ros2 topic echo /yolo/features std_msgs/msg/Float32MultiArray > "$COUNT_OUT" 2>/dev/null) &
ECHO=$!
sleep 1
timeout 3 ros2 topic pub -r 10 /yolo/detections image_processing_msgs/msg/DetectionArray "$DETECTIONS" > /dev/null 2>&1
wait "$ECHO"
N=$(grep -c "^---" "$COUNT_OUT")
if [ "$N" -ge 18 ]; then
    echo "PASS  R-4 default processes every frame ($N feature messages from ~30 detection frames)"
else
    echo "FAIL  R-4 default: only $N feature messages from ~30 detection frames (expected ~30)"; FAILED=1
fi
rm -f "$COUNT_OUT"; stop_node

# --- R-4: the rate is a parameter ---
run_node -p log_every_n_frames:=5
COUNT_OUT=$(mktemp)
(timeout 4 ros2 topic echo /yolo/features std_msgs/msg/Float32MultiArray > "$COUNT_OUT" 2>/dev/null) &
ECHO=$!
sleep 1
timeout 3 ros2 topic pub -r 10 /yolo/detections image_processing_msgs/msg/DetectionArray "$DETECTIONS" > /dev/null 2>&1
wait "$ECHO"
N5=$(grep -c "^---" "$COUNT_OUT")
if [ "$N5" -ge 3 ] && [ "$N5" -le 10 ]; then
    echo "PASS  R-4 log_every_n_frames:=5 thins the output ($N5 feature messages)"
else
    echo "FAIL  R-4 parameter: $N5 feature messages with log_every_n_frames:=5 (expected about 6)"; FAILED=1
fi
rm -f "$COUNT_OUT"; stop_node

exit $FAILED
