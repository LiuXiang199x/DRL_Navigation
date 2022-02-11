#!/usr/bin/env bash

echo "====> Init testing env <===="
source /home/agent/anaconda3/etc/profile.d/conda.sh
conda activate py3.6.9
source /opt/ros/noetic/setup.bash
export ROS_HOSTNAME=localhost
export ROS_MASTER_URI=http://localhost:11311
export ROS_PORT_SIM=11311
export GAZEBO_RESOURCE_PATH=~/ROS/DRL-robot-navigation/catkin_ws/src/multi_robot_scenario/launch
cd ~/ROS/DRL-robot-navigation/catkin_ws
source devel_isolated/setup.bash
cd ~/ROS/DRL-robot-navigation/TD3
echo "====> Testing env settled done <===="
