#!/usr/bin/env python

import rospy

from my_assignment.msg import PlanningActionResult

from my_assignment.srv import Counter,CounterResponse

reach_counter=0
cancel_counter=0

def count_printer(string):
	"""
    
    	Function for sending the response 
    
    	Parameters: string (string)
    
    	"""

	return CounterResponse(reach_counter,cancel_counter) #result

def res_cb(res):
	"""
    
    	Function for compute how many goals are reached or cancelled
    
    	Parameters: res (PlanningActionResult)
    
    	"""
	
	global reach_counter, cancel_counter
	
	if(res.status.status==3): #goal reached
		reach_counter+=1
	elif(res.status.status==2): #goal preempted
		cancel_counter+=1 
	

def main():

	rospy.init_node('counter') #start node
	
	rospy.Subscriber('/reaching_goal/result',PlanningActionResult,res_cb) #get info if goal is reached or not
	
	service=rospy.Service('counter',Counter,count_printer) #service
	
	rospy.spin()
	
	
	
if __name__=='__main__':

	try:
		
		main()
		
		
	except rospy.ROSInterruptException:
		
		print("\nError counter\n")
		exit()
