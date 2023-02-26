#!/usr/bin/env python

"""
.. module: counter
   :platform unix
   :synopsis: Python module for counting reached and cancelled goals
   
.. moduleauthor:: Luca Petruzzello <S5673449@studenti.unige.it>

This ROS node is used for computing the total of reached and cancelled goals using the info received from the /reaching_goal/result topic and for sending them to a client through the service /client.

Subscribes to:
  /reaching_goal/result

Clients:
  /counter


"""

import rospy

from my_assignment.msg import PlanningActionResult

from my_assignment.srv import Counter,CounterResponse

reach_counter=0
"""
global variable for counting reached goals

"""
cancel_counter=0
"""
global variable for counting cancelled goals

"""

def count_printer(string):
	"""
    
    	Function for sending the response 
    
    	Args: 
    	string (string): request from client
    	
    	Returns:
    	CounterResponse(integer): total number of reached and cancelled goals
    
    	"""

	return CounterResponse(reach_counter,cancel_counter) #result

def res_cb(res):
	"""
    
    	Function for compute how many goals are reached or cancelled
    
    	Args: 
    	res (PlanningActionResult): results regarding goals
    	
    	No Returns
    
    	"""
	
	global reach_counter, cancel_counter
	
	if(res.status.status==3): #goal reached
		reach_counter+=1
	elif(res.status.status==2): #goal preempted
		cancel_counter+=1 
	

def main():

	"""
	Function used for starting the node, for subscribing to /reaching_goal/result topic 
	and for the service /counter
	
	No Args
	
	No Returns
	
	"""

	rospy.init_node('counter') #start node
	
	rospy.Subscriber('/reaching_goal/result',PlanningActionResult,res_cb) 
	
	"""
	get info if goal is reached or not
	"""
	service=rospy.Service('counter',Counter,count_printer) #service
	
	rospy.spin()
	
	
	
if __name__=='__main__':

	try:
		
		main()
		
		
	except rospy.ROSInterruptException:
		
		print("\nError counter\n")
		exit()
