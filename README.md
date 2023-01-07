# Assignment-2

## Project Goal
Given a simulation, create an action client which gives the user the possibility to decide the robot's goal and which takes information from the topic /odom.
Create a service node that returns how many times the goal has been reached or cancelled.
Create a node that takes the information taken from the first node and prints out the distance to goal and the average speed.

## How to install and run

### Install

It is necessary to have ROS. Follow the instructions from [wiki.ros.org](http://wiki.ros.org/).

If you are using the professor's Docker Image, add the line ```source /opt/ros/noetic/setup.bash``` to the .bashrc file.

You need to use Git. Run: ```sudo apt-get install git```

Then run on your shell: ```git clone https://github.com/luk1897/Research_Track_1-Assignment-2```

### Run

Run this command on your shell: ```roslaunch my_assignment assignment_launcher.launcher```
