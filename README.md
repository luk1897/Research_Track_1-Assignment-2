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

## Nodes

### Planning Client

This node gives the user the possibility to decide the robot's goal and which takes information from the topic /odom.

#### Publish_function

```python
def publish_function(od):

	pub=rospy.Publisher('/posvel',Posvel,queue_size=10) # publisher on /posvel topic
	
	info=Posvel() 
	
	info.x=od.pose.pose.position.x
	
	info.y=od.pose.pose.position.y 
	
	info.vel_x=od.twist.twist.linear.x 
	
	info.vel_z=od.twist.twist.angular.z 
	
	pub.publish(info)
  ```
  
  This function for publish Posvel custom message (created with odometry information) on /posvel topic.
  
  #### Menu
  
  ```python
  def menu(client):

	print("MENU\n")
	print("1. Choose your goal\n")
	print("2. Cancel your goal\n")
	print("3. Number of reached and cancelled goals\n")
	print("4. Exit\n")
	
	print("Insert your choice: \n")
	choice=int(input())
	
	if(choice == 1):
		goal = position() #getting goal coordinates
		client.send_goal(goal) #sending goal to the server
		print("Goal sent!\n")
		
	elif(choice == 2):
		client.cancel_goal() #cancelling goal
		print("\nGoal cancelled!\n")
		
	elif(choice == 3):
		rospy.wait_for_service('counter') #synchronizing with service node
		
		service=rospy.ServiceProxy('counter',Counter) #request to the service node
		
		counter=service("ok") # used a message "ok" to avoid any problem with empty message
	
	elif(choice == 4):
		print("\nExiting!\n")
		exit()
```

The function for choosing the goal, cancelling it and showing the number of reached and cancelled goals.

#### Position

``` python
def position():
	
	print("Insert x value: " )
	
	x=float(input())
	
	print("Insert y value: " )
	
	y=float(input())
	
	print("\nGoal: (%s,%s) "%(x,y))
	print("\n")
	
	goal=PlanningGoal()  #initialising goal to the message PlanningGoal
	
	goal.target_pose.pose.position.x=x #set the x goal position
		
	goal.target_pose.pose.position.y=y #set the y goal position
	
	return goal
```

The function for getting goal coordinates.
