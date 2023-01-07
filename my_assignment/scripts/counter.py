#!/usr/bin/env python

import rospy

from my_assignment.msg import PlanningActionFeedback,PlanningActionResult

from my_assignment.srv import Counter,CounterResponse

reach_counter=0
cancel_counter=0

#def status_counter(feed):
	

#	global reach_counter
#	global cancel_counter

#	if(feed.feedback.stat=="Target reached!"):
#		reach_counter+=1
#	elif(feed.feedback.stat=="Target cancelled!"):
#		cancel_counter+=1 

def count_printer(string):
	"""
    
    	Function for compute how much goal is reached or cancelled
    
    	Parameters: feed (PlanningActionResult)
    
    	"""

	print("\nreached goal: %s and cancelled goal: %s\n" %(reach_counter,cancel_counter))
	
	return CounterResponse(reach_counter,cancel_counter) #result

def res_cb(res):
	"""
    
    	Function for compute how much goal is reached or cancelled
    
    	Parameters: feed (PlanningActionFeedback)
    
    	"""
	
	global reach_counter, cancel_counter
	
	if(res.status.status==3):
		reach_counter+=1
	elif(res.status.status==2):
		cancel_counter+=1 
	

def main():

	rospy.init_node('counter') #start node

	#rospy.Subscriber('/reaching_goal/feedback',PlanningActionFeedback,status_counter) #get info if goal is reached or not
	rospy.Subscriber('/reaching_goal/result',PlanningActionResult,res_cb) #get info if goal is reached or not
	
	service=rospy.Service('counter',Counter,count_printer) #service
	
	rospy.spin()
	
	
	
if __name__=='__main__':

	try:
		
		main()
		
		
	except rospy.ROSInterruptException:
		
		print("\nError counter\n")
		exit()
