# **ENPM690 – Homework 3: Robot Teleoperation and Autonomous Navigation**


## Table of Contents
1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Environment Setup](#environment-setup)
4. [Install](#install)
5. [Running Simulations](#running-simulations)
6. [License](#license)

## **Overview**
For homework assignment 3, I have created a simple teleoperation and autonomous navigation simulation using ROS2 and Webots. The project is broken down into two main ROS packages: 1. The ROS2 package handling the environment, robot, and robot driver setup and 2. The ROS2 pakcage that performs the teleoperation and autonomous navigation (this repository).

## **Dependencies**
This project has several dependencies that are required in order to run the simulations. Installing these dependencies are outside the scope of this project however, some useful installation information can be found below.

This project depends on:
- **ROS2 Jazzy**: Installation documentation found here [link](https://docs.ros.org/en/jazzy/Installation.html)
- **Webots Simulator**: Installation documentation found here [link](https://cyberbotics.com/doc/guide/installation-procedure)
- **Catch2 Integration**: Install after setting up ROS2 using the following command

```sh
source /opt/ros/humble/setup.bash  # if needed
apt install ros-${ROS_DISTRO}-catch-ros2
```
## **Environment Setup**
Before you can install the required packages to run the simulation you must first create a ROS2 workspace. The following steps assume you have all necessary project dependencies.

### Create a ROS2 workspace
Navigate to where you would like to create your ROS2 workspace and run the following:
```sh
# Source ROS2 underlay
source /opt/ros/jazzy/setup.bash

# Create ROS2 workspace directory
mkdir ros2_ws
cd ros2_ws/
mkdir src
cd src/
cd ..

# Build workspace
colcon build
```

## **Install**
To install all the necessary packages navigate to the root of your ROS2 workspace and run the following commands:
```sh
# Source ROS2 underlay
source /opt/ros/jazzy/setup.bash

# Clone repositories
cd src/
git clone https://github.com/GraysonGilbert/my_webots_tutorials.git
git clone https://github.com/GraysonGilbert/enpm690_hw3.git
cd ..

# Build packages
colcon build
```
## **Running Simulations**

There are two different simulations to run for this project assignment. The first simulation controls the robot through teleoperation. The second simulation autonomously navigate the robot around the environment.


### Teleop Simulation:
Navigate the robot around the simulation world by using the keys (a, s, w, d, and [space bar])


To the run the teleoperation simulation, you must first have two terminals open at the root of the ROS2 workspace. Then run the following commands:
#### Run this in the 1st terminal
```sh
# Source ROS2 underlay
source /opt/ros/jazzy/setup.bash

# Start teleop simulation 
ros2 launch enpm690_hw3 teleop.launch.py 
```
#### Run this in the 2nd terminal
```sh
# Source ROS2 underlay
source /opt/ros/jazzy/setup.bash

# Run teleop node
ros2 run enpm690_hw3 teleop.py 
```

### Autonomous Navigation Simulation
#### Run this in the 1st terminal
```sh
# Source ROS2 underlay
source /opt/ros/jazzy/setup.bash

# Start teleop simulation 
# sensor_threshold is a tunable parameter. Input a value between [0, 0.15] to change 
# the distance at which the robot will recognize an obstacle and move around it
ros2 launch enpm690_hw3 autonomous_nav.launch.py sensor_threshold:=0.12
```


## **License**
This project is licensed under the **MIT Licencse**.