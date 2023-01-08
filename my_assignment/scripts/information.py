#!/usr/bin/env python


from __future__ import print_function

import rospy,numpy

from my_assignment.msg import Posvel, PlanningActionGoal

goal_x=0.0
goal_y=0.0

distance_x=0.0
distance_y=0.0

average_vel_x=0.0
average_vel_z=0.0

vel_x_list=[]
vel_z_list=[]

def goal_cb(pos):
	"""
    
    	Function for getting current goal
    
    	Parameters: pos (PlanningActionGoal)
    
    	"""

	global goal_x,goal_y

	goal_x=pos.goal.target_pose.pose.position.x	#x goal position
	goal_y=pos.goal.target_pose.pose.position.y	#y goal position
	

def posvel_cb(current):
	"""
    
    	Function for getting distance from current goal and velocity average
    
    	Parameters: current (Posvel)
    
    	"""

	global distance_x,distance_y,average_vel_x,average_vel_z,vel_x_list,vel_z_list
	
	dist_x=goal_x-current.x #distance x
	
	dist_y=goal_y-current.y #distance y
	
	distance_x=round(abs(dist_x),4)
	
	distance_y=round(abs(dist_y),4)
	
	vel_x_list.append(current.vel_x) #list with x velocity
	
	average_vel_x=sum(vel_x_list)/len(vel_x_list) #compute x velocity average
	
	vel_z_list.append(current.vel_z) #list with z velocity
	
	average_vel_z=sum(vel_z_list)/len(vel_z_list) #compute x velocity average
	

def main():
	
	freq=rospy.get_param("/frequency") #get parameter for frequence
	
	rate=rospy.Rate(freq) #set frequence
	
	rospy.Subscriber('reaching_goal/goal',PlanningActionGoal,goal_cb)  #get current goal
	
	rospy.Subscriber('/posvel',Posvel,posvel_cb) #get current position and velocity in order to compute distance from goal and velocity average
	
	while not rospy.is_shutdown():
	
		print("\ngoal distance: (%s,%s) "%(distance_x,distance_y))
		
		print("average x velocity: ",round(average_vel_x,4))
		
		print("average z velocity: ",round(average_vel_z,4))
		
		rate.sleep()

	


if __name__=="__main__":

	try:
		rospy.init_node('information')
		
		main()
		
		
	except rospy.ROSInterruptException:
		
		print("Error info")
		exit()
