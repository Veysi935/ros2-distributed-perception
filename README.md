# ROS 2 Distributed Perception Pipeline (YOLOv8 + TurtleBot3)

A custom ROS 2 Jazzy perception package (`edge_perception`) that integrates real-time **YOLOv8** object detection with a **TurtleBot3** simulation in **Gazebo Harmonic**. This repository represents the perception layer of a full-stack robotics workflow covering SLAM, Nav2 autonomous navigation, and edge AI vision.

## System Architecture

1. **Simulation Layer (Gazebo Harmonic):** Runs TurtleBot3 Waffle with an RGB camera publishing raw frames to `/camera/image_raw`.
2. **Bridge & Transport (ROS 2 Jazzy):** Uses `ros_gz_bridge` and `cv_bridge` to convert ROS 2 `sensor_msgs/Image` messages into OpenCV `bgr8` frames.
3. **Inference Layer (`yolo_node.py`):** Subscribes to `/camera/image_raw`, runs real-time inference using **YOLOv8n (PyTorch)**, and renders bounding boxes with dynamic confidence scores.

## Tech Stack

- **OS & Environment:** Ubuntu 24.04 (WSL2)
- **Robotics Middleware:** ROS 2 Jazzy Jalisco
- **Simulation:** Gazebo Harmonic, TurtleBot3
- **Computer Vision & AI:** Python 3.12, OpenCV, CvBridge, PyTorch, Ultralytics YOLOv8

## Installation & Usage

### 1. Prerequisites
Ensure ROS 2 Jazzy, TurtleBot3 Gazebo packages, and `ultralytics` are installed:

```bash
sudo apt install ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-image ros-jazzy-cv-bridge -y
python3 -m pip install ultralytics --break-system-packages
```

### 2. Build the Package
Clone this repository into your ROS 2 workspace `src` directory and build:

```bash
mkdir -p ~/colcon_ws/src
cd ~/colcon_ws/src
git clone [https://github.com/Veysi935/ros2-distributed-perception.git](https://github.com/Veysi935/ros2-distributed-perception.git) edge_perception
cd ~/colcon_ws
colcon build
source install/setup.bash
```

### 3. Run the Pipeline

**Terminal 1 — Launch Gazebo Simulation:**
```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

**Terminal 2 — Start the YOLOv8 Perception Node:**
```bash
source ~/colcon_ws/install/setup.bash
ros2 run edge_perception yolo_node
```

**Terminal 3 — Control the Robot (Teleop):**
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

## Engineering Observation: The Sim-to-Real Gap

During testing in the default Gazebo world, YOLOv8 (pretrained on the real-world COCO dataset) occasionally misclassifies low-poly, textureless 3D cylinders as objects like `refrigerator` or `tv`. However, as the robot approaches target objects, bounding boxes stabilize and confidence scores scale dynamically—confirming low-latency, real-time end-to-end processing across the ROS 2 to PyTorch pipeline.
