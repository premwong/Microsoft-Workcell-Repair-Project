#!/usr/bin/env python

import rospy
import serial as ps

from std_msgs.msg import String
from iiwa_msgs.srv import MoveConveyor

def handle_move_conveyor(req):
	print("Trying to move with the below command: ")
	print(bytearray(req.command))

	try: 
		ser = ps.Serial('/dev/ttyACM0', 9600, timeout=0)
		ser.write(bytearray(req.command))
		ser.close()
	except ps.SerialException as e:
		print(e)
		return 0
	return 1
    
def move_conveyor_server():
	rospy.init_node('conveyor_server')
	service = rospy.Service('move_conveyor', MoveConveyor, handle_move_conveyor)
	rospy.spin()

if __name__=='__main__':
	move_conveyor_server()
