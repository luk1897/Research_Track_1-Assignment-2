# Assignment-2

## Project Goal

Given a simulation, create an action client which gives the user the possibility to decide the robot's goal and which takes information from the topic /odom.
Create a service node that returns how many times the goal has been reached or cancelled.
Create a node that takes the information taken from the first node and prints out the distance to goal and the average speed.

## IMPORTANT 

I modified the launcher of the package assignment_2_2022 by adding ```launch-prefix="xterm"``` to the bug_as.py node to get info on the behaviour of the robot in another console. 
I added ```launch-prefix="xterm"```, also in the launcher of the package my_assignment, to the information.py node to have a cleaner output.

## How to install and run

### Install

It is necessary to have ROS. Follow the instructions from [wiki.ros.org](http://wiki.ros.org/).

If you are using the professor's Docker Image, add the line ```source /opt/ros/noetic/setup.bash``` to the .bashrc file.

You need to use Git. Run: ```sudo apt-get install git```

Then run on your shell: ```git clone https://github.com/luk1897/Research_Track_1-Assignment-2```

Then install xterm. Run ```sudo apt-get install xterm```

### Run

Run this command on your shell: ```roslaunch my_assignment assignment_launcher.launcher```

## Environment

![environment rt1](https://user-images.githubusercontent.com/80416766/211173168-53474ace-d147-4405-bc21-82d217790b63.png)

This is the entire environment in which I worked.

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

The function is useful for getting goal coordinates.

#### Output 

![client_console](https://user-images.githubusercontent.com/80416766/211173202-07822132-67b0-4e38-8657-f566f7a6d977.png)

### Information

This node a node takes the information taken from the first node and prints out the distance to goal and the average speed.

#### Posvel_cb

``` python
def posvel_cb(current):

	global distance_x,distance_y,average_vel_x,average_vel_z,vel_x_list,vel_z_list
	
	dist_x=goal_x-current.x 
	
	dist_y=goal_y-current.y 
	
	distance_x=round(abs(dist_x),4)
	
	distance_y=round(abs(dist_y),4)
	
	vel_x_list.append(current.vel_x) 
	
	average_vel_x=sum(vel_x_list)/len(vel_x_list) 
	
	vel_z_list.append(current.vel_z) 
	
	average_vel_z=sum(vel_z_list)/len(vel_z_list)
```

This function is used for getting distance from current goal and velocity average.

#### Goal_cb

```
def goal_cb(pos):
	global goal_x,goal_y

	goal_x=pos.goal.target_pose.pose.position.x	#x goal position
	goal_y=pos.goal.target_pose.pose.position.y	#y goal position
```
This Function is useful for getting current goal.

#### Output

![info_console](https://user-images.githubusercontent.com/80416766/211173208-e70b2e37-eec2-4620-828d-3e0900c6ea8b.png)

## Pseudocode of planning_client (node a)

```
function position without parameters
	print "Insert x value: "
	get x coordinate from user
	print "Insert y value: "
	get y coordinate from user
	print "Goal coordinates"
	initialising goal to the message PlanningGoal
	set the x goal coordinate
	set the y goal coordinate
	return the goal

function menu with parameter client (PlanningAction)
	printing the possible choices
	print "Insert your choice: "
	get the number which represents the choice of the user
	if the choice is 1
		call the function position which returns the goal
		send the goal to the server
		print "Goal sent!"
	endif
	else if the choice is 2
		cancel the current goal
		print "Goal cancelled!"
	end else if
	else if choice is 3
		synchronizing with the serve
		make request to the sevice node
		return the value of the goal reached and cancelled counters
	end else if
	else if  choice is 4
		print "Exiting"
		exit from the process
	end else if

function publish_function with parameter od (Odometry message)
	create publisher of the /posvel topic
	initialising info to the message Posvel
	set x coordinate of info to the current x position got from /odom topic
	set y coordinate of info to the current y position got from /odom topic
	set x velocity of info to the current x velocity got from /odom topic
	set z velocity of info to the current z velocity got from /odom topic
	send info to the /posvel topic

function main without parameters
	start the action client
	call the subscriber of /odom topic
	while ROS is not shutting down
		synchronizing client and server
		call the menu function
```

##  Possibile improvements
* It would be more useful to have all the robot information in one console, but a solution would have to be found regarding the readability of the information itself, as there would be little order.

* It might be useful to have the service node called up automatically after a predefined time so that it always shows the information about the achieved and deleted goals.
	
	
	
	
	
	
	
	
