#!/usr/bin/env bash
# Integration test for the copilot bridge over real ROS topics (run inside WSL after colcon build).
# Case 1: mock mode answers a question grounded in /game/state.
# Case 2: no mock and no OPENAI_API_KEY -> a clear "offline" answer (never a crash, never a hang).
# Usage: scripts/test_copilot_integration.sh
source /opt/ros/humble/setup.bash
source ~/unity_ws/install/setup.bash
source ~/ros2_px4_offboard_example_ws/install/setup.bash

FAILED=0
PIDS=()
cleanup() { for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null; done; pkill -f "image_processing/copilot_bridge" 2>/dev/null; }
trap cleanup EXIT

run_case() {
    local name="$1" expect_source="$2" expect_text="$3"; shift 3
    pkill -f "image_processing/copilot_bridge" 2>/dev/null; sleep 1
    local out; out=$(mktemp)

    env -u OPENAI_API_KEY ros2 run image_processing copilot_bridge --ros-args "$@" > /tmp/copilot_bridge_test.log 2>&1 &
    local bridge=$!; PIDS+=("$bridge")
    sleep 3

    ros2 topic pub -r 5 /game/state std_msgs/msg/String "{data: '{\"found\": 2, \"total\": 8, \"timeRemaining\": 90}'}" > /dev/null 2>&1 &
    local state=$!; PIDS+=("$state")
    sleep 1

    timeout 15 ros2 topic echo --once /copilot/answer std_msgs/msg/String --field data > "$out" 2>/dev/null &
    local echo_pid=$!
    sleep 2
    ros2 topic pub --once /copilot/question std_msgs/msg/String "{data: '{\"id\": \"t1\", \"text\": \"how many left?\", \"persona\": \"default\"}'}" > /dev/null 2>&1
    wait "$echo_pid"

    if grep -q "\"id\": \"t1\"" "$out" && grep -q "\"source\": \"$expect_source\"" "$out" && grep -q "$expect_text" "$out"; then
        echo "PASS  $name"
    else
        echo "FAIL  $name"; echo "  answer: $(cat "$out")"; FAILED=1
    fi
    # `ros2 run` leaves its child node alive when the wrapper is killed, so stop the bridge itself between cases
    kill "$bridge" "$state" 2>/dev/null; pkill -f "image_processing/copilot_bridge" 2>/dev/null; wait "$bridge" "$state" 2>/dev/null; sleep 1
    rm -f "$out"
}

run_case "mock answer is grounded in game state" mock "2 of 8" -p mock:=true
run_case "no key -> offline answer"                offline "offline"

exit $FAILED
