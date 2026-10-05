# gz-px4-yolo-objectDetection

A ROS 2 pipeline for **vision-based object detection and object-relative flight control** on a simulated PX4 quadcopter in **Gazebo Harmonic**.

The drone's onboard camera feed is bridged from Gazebo into ROS 2, run through a YOLO object detector, and the detections are scored to choose the most prominent object in view. The drone's pose and that target are then used by a PID-based behavior node that sends velocity setpoints to PX4 over the Micro XRCE-DDS bridge, so the drone flies to and holds a standoff position relative to the detected object.

```
 Gazebo Harmonic (PX4 SITL, x500_depth)
        │  /camera  (gz.msgs.Image)
        ▼
 ros_gz_bridge ──► /camera/image_raw ──► yolo_subscriber ──► /yolo/detections ──► behavior_controller
                                              │                                        │
                                              ▼                                        ├─► /behavior/prominent_object
                                   /yolo/image_annotated (RViz)                        ├─► /behavior/prominent_array
                                                                                       └─► /yolo/features
 PX4 (uXRCE-DDS) ──► /fmu/out/* ──► visualizer ──► /px4_visualizer/vehicle_pose ──► drone_pose_publisher ──► /drone/pose
                                                                                                                │
                                                       distance_predictor_xyz ◄────────────────────────────────┘
                                                                │ /object_distance_xyz
                                                                ▼
                                                      drone_behavior_node (PID + yaw)
                                                                │ /fmu/in/trajectory_setpoint
                                                                ▼
                                                              PX4
```

---

## Features

- **Gazebo Harmonic ↔ ROS 2 camera bridge** via `ros_gz_bridge` (`/camera` → `/camera/image_raw`).
- **YOLO object detection** (Ultralytics YOLOv8 / YOLO11) with annotated image output for RViz.
- **Custom detection messages** (`Detection`, `DetectionArray`, `ProminentObject`, `ProminentObjectArray`) with bounding box, center, size and confidence.
- **Prominent-object selection**: each detection is scored with a sigmoid-weighted confidence term plus a normalized pixel-area term, and smoothed over a short history window.
- **Object-relative flight control**: PID controllers on X/Y/Z drive the drone to a desired offset from the target, with yaw steering from the target's horizontal offset in the image.
- **PX4 offboard control** with an arm → takeoff → loiter → offboard state machine and keyboard teleoperation (based on [ARK Electronics' ROS2_PX4_Offboard_Example](https://github.com/ARK-Electronics/ROS2_PX4_Offboard_Example)).
- **RViz visualization** of vehicle pose, path, setpoint path and velocity.
- **Data collection tools**: a keyboard-driven image labeler for building datasets, and a CSV dataset (`ImprovedDistanceEstimatorData.csv`, ~6,200 samples) of detection features vs. ground-truth distances used to train an ML distance estimator.

---

## Repository layout

```
.
├── ImprovedDistanceEstimatorData.csv     # Detection features → ground-truth XYZ distance dataset
└── src/
    ├── ROS2_PX4_Offboard_Example/
    │   └── px4_offboard/                 # PX4 offboard control, teleop, visualizer, launch file
    ├── image_processing/                 # Detection, scoring, distance and behavior nodes + models
    │   ├── image_processing/             # Python nodes
    │   ├── YOLOv8/best.pt                # Custom-trained YOLOv8 weights (default)
    │   ├── YOLOv11_1.0/yolo11n.pt        # YOLO11 nano weights
    │   ├── yolo_model_export/            # YOLO11 run exported to .pt / .onnx / .engine + class names
    │   ├── 2class.pth                    # ForestCNN forest / no-forest classifier
    │   └── distance_model_light.pkl      # Trained distance regression model
    ├── image_processing_msgs/            # Custom ROS 2 message definitions
    └── px4_msgs/                         # PX4 ROS 2 message definitions (submodule)
```

---

## Packages and nodes

### `image_processing`

| Executable | Description | Subscribes | Publishes |
|---|---|---|---|
| `yolo_subscriber` | Runs Ultralytics YOLO on each camera frame and publishes structured detections plus an annotated image. | `/camera/image_raw` | `/yolo/detections` (`DetectionArray`), `/yolo/image_annotated` (`Image`) |
| `yolov11_subscriber` | Alternative detector using the exported YOLO11 **ONNX** model through ONNX Runtime (CPU). Publishes an annotated image only. | `/camera/image_raw` | `/yolo/image_annotated` |
| `behavior_controller` | Scores every detection, picks the most prominent object, smooths it over the last 5 frames, and publishes the feature vector used by the distance estimator. | `/yolo/detections`, `/drone/pose`, `/camera/image_raw` | `/yolo/prominent`, `/behavior/prominent_object`, `/behavior/prominent_array`, `/yolo/features` |
| `drone_pose_publisher` | Republishes the PX4 visualizer pose on a simpler topic. | `/px4_visualizer/vehicle_pose` | `/drone/pose` |
| `distance_predictor_xyz` | Publishes the XYZ vector between the drone and the target object (currently a known world position; the ML-based predictor is kept in comments for reference). | `/drone/pose` | `/object_distance_xyz` (`Float32MultiArray`) |
| `drone_behavior_node` | PID controller that flies the drone to a desired offset (default `[2, 2, -3]` m) from the target and yaws toward it. Runs at 20 Hz. | `/drone/pose`, `/object_distance_xyz`, `/yolo/features` | `/fmu/in/trajectory_setpoint` |
| `image_subscriber` | Forest / no-forest scene classification with a small CNN (`ForestCNN`, `2class.pth`). | `/camera/image_raw` | — (logs prediction) |
| `image_labeler` | Keyboard tool for saving camera frames into labeled folders (`c` car, `p` person, `b` building, `t` tree). | `/camera/image_raw` | — (writes `.jpg` files) |

**Prominence score.** For each detection:

```
score = conf_weight · sigmoid(confidence; k, x0) + area_weight · (pixel_area / max_pixel_area)
```

Defaults in the node are `k = 15`, `x0 = 0.5`, `conf_weight = 0.6`, `area_weight = 0.4`. A grid of `k`, `x0` and weight pairs is defined in the node for parameter sweeps.

**`drone_behavior_node` parameters**

| Parameter | Default | Meaning |
|---|---|---|
| `rotate_to_body_frame` | `False` | Rotate world-frame velocities into the vehicle body frame before publishing. |
| `rotate_yaw_sign` | `-1` | Rotation direction used when `rotate_to_body_frame` is true. |

### `image_processing_msgs`

| Message | Fields |
|---|---|
| `Detection` | `class_name`, `confidence`, `x_min`, `y_min`, `x_max`, `y_max`, `x_center`, `y_center`, `width`, `height`, `pixel_area` |
| `DetectionArray` | `Detection[] detections` |
| `ProminentObject` | `class_name`, `x_center`, `y_center`, `size_score` |
| `ProminentObjectArray` | `ProminentObject[] objects` |

### `px4_offboard`

| Executable | Description |
|---|---|
| `processes` | Opens terminal tabs running `MicroXRCEAgent udp4 -p 8888` and `make px4_sitl gz_x500_depth`. |
| `control` | Keyboard teleop (Mode 2): `W/S` up/down, `A/D` yaw, arrow keys pitch/roll, `Space` arm/disarm. Publishes `/offboard_velocity_cmd` and `/arm_message`. |
| `velocity_control` | Offboard state machine (IDLE → ARMING → TAKEOFF → LOITER → OFFBOARD) that publishes `OffboardControlMode`, `TrajectorySetpoint` and `VehicleCommand` to PX4. |
| `visualizer` | Converts PX4 NED state to ENU and publishes pose, path, setpoint path and velocity marker for RViz. |

The launch file `offboard_velocity_control.launch.py` starts `visualizer`, `processes`, `control`, `velocity_control`, the `ros_gz_bridge` camera bridge, `yolo_subscriber`, `drone_pose_publisher` and RViz.

---

## Detection models

| Model | Path | Notes |
|---|---|---|
| YOLOv8 (custom) | `src/image_processing/YOLOv8/best.pt` | Default model loaded by `yolo_subscriber`. |
| YOLO11 nano | `src/image_processing/YOLOv11_1.0/yolo11n.pt` | Alternative, commented in `yolo_subscriber`. |
| YOLO11 (custom export) | `src/image_processing/yolo_model_export/content/runs/detect/train/weights/` | `best.pt`, `best.onnx`, `best.engine`. Trained on the Roboflow dataset [drone-research/truckbuildingedited v6](https://universe.roboflow.com/drone-research/truckbuildingedited/dataset/6) (CC BY 4.0) with 5 classes: **Building, Car, Forest, Person, Truck**. |

---

## Requirements

- **Ubuntu 22.04** with **ROS 2 Humble**
- **Gazebo Harmonic** and the matching `ros_gz` packages (`ros_gz_bridge`)
- **PX4-Autopilot** (SITL) cloned to `~/PX4-Autopilot`
- **Micro XRCE-DDS Agent** (`MicroXRCEAgent`)
- `gnome-terminal` (used by the launch file to open nodes in separate windows)
- Optional: QGroundControl
- Python packages:

```bash
pip install ultralytics torch torchvision "numpy<2" "opencv-python-headless<4.9" onnxruntime joblib
```

---

## Build

```bash
mkdir -p ~/ros2_px4_offboard_example_ws
cd ~/ros2_px4_offboard_example_ws
git clone --recurse-submodules https://github.com/calebabr/gz-px4-yolo-objectDetection.git .
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

If `src/px4_msgs` is empty, clone it manually and check out the branch that matches your PX4 version:

```bash
git clone https://github.com/PX4/px4_msgs.git src/px4_msgs
```

> **Important:** Several nodes load models and write data using absolute paths under `/home/cjabrantes/ros2_px4_offboard_example_ws/src/image_processing/`. Update those paths (in `yolo_subscriber.py`, `yolov11_subscriber.py`, `image_subscriber.py` and `image_labeler.py`) to match your workspace before building.

---

## Running

### Full pipeline

```bash
ros2 launch px4_offboard offboard_velocity_control.launch.py
```

This starts the Micro XRCE-DDS agent and PX4 SITL in Gazebo Harmonic (`gz_x500_depth`), the camera bridge, YOLO detection, pose republishing, offboard control and RViz. In the teleop window, press **Space** to arm; the drone will take off, loiter, and switch to offboard mode.

Then, in separate terminals (each with `source install/setup.bash`), start the scoring and autonomous behavior nodes:

```bash
ros2 run image_processing behavior_controller
```

```bash
ros2 run image_processing distance_predictor_xyz
```

```bash
ros2 run image_processing drone_behavior_node
```

### Individual nodes

```bash
ros2 run image_processing yolo_subscriber
ros2 run image_processing yolov11_subscriber
ros2 run image_processing image_labeler
ros2 run image_processing image_subscriber
```

### Bridging the camera manually

```bash
ros2 run ros_gz_bridge parameter_bridge /camera@sensor_msgs/msg/Image@gz.msgs.Image --ros-args --remap /camera:=/camera/image_raw
```

### Useful topics to inspect

```bash
ros2 topic echo /yolo/detections
ros2 topic echo /behavior/prominent_object
ros2 topic echo /object_distance_xyz
```

View `/yolo/image_annotated` in RViz or `rqt_image_view` to see the bounding boxes live.

---

## Distance estimation dataset

`ImprovedDistanceEstimatorData.csv` contains detection features logged by `behavior_controller` alongside ground-truth distances from the simulator:

| Column | Description |
|---|---|
| `pred_conf` | Detector confidence |
| `pred_area` | Bounding box pixel area |
| `score` | Prominence score |
| `width`, `height`, `aspect_ratio` | Bounding box geometry |
| `distance_x`, `distance_y`, `distance_z` | Ground-truth distance from the drone to the object |

This data was used to train `distance_model_light.pkl`, a lightweight regressor that predicts the drone-to-object distance from detection features alone. The inference code is preserved (commented) in `distance_predictor_xyz.py`.

---

## Notes and limitations

- The target object's world position (`casual_female` in the Baylands world) is hard-coded in `behavior_controller` and `distance_predictor_xyz` for ground truth and control.
- `yolov11_subscriber` does not apply non-maximum suppression and does not publish a `DetectionArray`.
- PX4 uses NED coordinates; the visualizer converts to ENU for RViz, and `drone_behavior_node` flips Z when publishing setpoints.
- Test in simulation before flying any of this on real hardware.

---

## Acknowledgments

- [ARK Electronics – ROS2_PX4_Offboard_Example](https://github.com/ARK-Electronics/ROS2_PX4_Offboard_Example) (Braden Wagstaff) for the offboard control and teleop base
- PX4 visualizer by Jaeyoung Lim
- [PX4 Autopilot](https://px4.io/), [Gazebo](https://gazebosim.org/), [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- Training data from [Roboflow Universe – drone-research](https://universe.roboflow.com/drone-research/truckbuildingedited/dataset/6)
