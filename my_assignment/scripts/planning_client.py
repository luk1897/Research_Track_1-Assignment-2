#!/usr/bin/env python

from __future__ import print_function

import rospy,actionlib

from my_assignment.msg import PlanningAction, PlanningGoal,Posvel

from nav_msgs.msg import Odometry

from my_assignment.srv import Counter

def position():
	"""
    
    	Function for getting goal coordinates
    
    	Return: goal (PlanningGoal)
    
    	"""
	
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
	
	
def menu(client):
	"""
    
    	Function for choosing the goal, cancelling it and
    	showing the number of reached and cancelled goals
    
    	Parameteres: client (PlanningAction)
    
    	"""

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
		rospy.loginfo("Goal sent!\n")
		
	elif(choice == 2):
		client.cancel_goal() #cancelling goal
		rospy.loginfo("Goal cancelled!\n")
		
	elif(choice == 3):
		rospy.wait_for_service('counter') #synchronizing with service node
		
		service=rospy.ServiceProxy('counter',Counter) #request to the service node
		
		counter=service("ok") # used a message "ok" to avoid any problem with empty message
		rospy.loginfo("reached goal: %s and cancelled goal: %s\n" %(counter.total_reach,counter.total_cancel))
	
	elif(choice == 4):
		rospy.loginfo("Exiting!\n")
		exit()


def publish_function(od):
	"""
    
    	Function for publish Posvel custom message (created with odometry information)
    	on /posvel topic
    
    	Parameteres: od (Odometry message)
    
    	"""

	pub=rospy.Publisher('/posvel',Posvel,queue_size=10) # publisher on /posvel topic
	
	info=Posvel() #initialising info to the custom message Posvel
	
	info.x=od.pose.pose.position.x #get x position from /odom topic
	
	info.y=od.pose.pose.position.y #get y position from /odom topic
	
	info.vel_x=od.twist.twist.linear.x #get x linear velocity from /odom topic
	
	info.vel_z=od.twist.twist.angular.z #get z angular velocity from /odom topic
	
	pub.publish(info) # publish info on /posvel topic


def main():
	
	client=actionlib.SimpleActionClient('reaching_goal',PlanningAction) #necessary to start the client
	
	rospy.Subscriber('/odom',Odometry,publish_function) #subscribing to /odom topic
	
	while not rospy.is_shutdown():
	
		client.wait_for_server() #synchronizing client and server
		
		menu(client) #calling the menu function
		
		
		
	
if __name__=='__main__':

	try:
		rospy.init_node('planning_client') #necessary to start the node
		
		main()
		
		
	except rospy.ROSInterruptException:
		
		print("Error client")
		exit()
