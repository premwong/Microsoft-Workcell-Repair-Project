#!/usr/bin/env python
"""
@Author: Nano Premvuti @premwong
University of Washington 2020
Department of Electrical & Computer Engineering
"""
import sys
import rospy
from workcell_iiwa_control import MoveGroupLeftArm
from std_msgs.msg import Float64MultiArray
from iiwa_msgs.srv import MoveConveyor

class ItemState(object):
	"""item that holds components eg. server, tray, etc"""
	def __init__(self, item_id, item_type):
		super(ItemState, self).__init__()
		self._item_id = item_id
		self._item_type = item_type
		self._heatsink1 = True
		self._heatsink2 = True
		self._nic = True
		self._hdd1 = True
		self._hdd2 = True
		self._dimm1 = True
		self._dimm2 = True

	def get_parts_list(self):
		return self.__dict__

def replace_nic(move_group, server_item, tray_item):
	move_group.print_state()
	try:
		print " Press to start sequence"
		raw_input()
		move_group.goto_component_position('nic')
		move_group.set_gripper(True)
		rospy.sleep(2)
		move_group.extend_trajectory(-0.06)
		rospy.sleep(1)
		move_group.set_gripper(False)
		rospy.sleep(0.5)
		move_group.extend_trajectory(0.06)
		
	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return

def replace_heatsink(server, move_group):
	try:
		print "Press to start heatsink sequence"
		raw_input()
		move_group.goto_cartesian_state(0.1, 0.7, 0.2, 0, 'heatsink')
	except rospy.ROSInterruptException:
		return
	except KeyboardInterrupt:
		return

def autostop_callback(camera_feed):
	print 'hi'
	camera_feed_buffer = camera_feed.data
	if camera_feed_buffer[6] <= 200:
		move_conveyor("S")

rospy.init_node('user_control')
rospy.Subscriber('camera_pose_feed', Float64MultiArray, autostop_callback)
print 'waiting for conveyor service...'
rospy.wait_for_service('move_conveyor')
try:
	move_conveyor = rospy.ServiceProxy('move_conveyor', MoveConveyor)
	print 'hello conveyor'
except rospy.ServiceException as e:
	print(e)

def main():
	try:
		# myLeftArm = MoveGroupLeftArm()

		# myLeftArm.load_component_map()
		# myLeftArm.print_state()
		# # myLeftArm.goto_fiducial_position()
		# # myLeftArm.goto_cartesian_state(0.1, 0.7, 0.25, -30, 'nic1')
		# rospy.sleep(4)
		# # myLeftArm.execute_trajectory_from_file('nic_to_heatsink1')
		# # rospy.sleep(8)
		# myLeftArm.gotoartesian_state(0.0, 0.6, 0.25, 90, 'heatsink1')
		move_conveyor("F")
		rospy.spin()

	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return

if __name__ == '__main__':
  main()



#Example control flow:
# welcome to the server repair workcell
# starting etc...
# waiting for server mover .... (press ENTER to override)
# server mover arrived!
# retracting conveyor belt...
# server id:... heatsink: old... nic: old... etc...

# Select option to replace: [1] nic card [2] heatsink [3] _hdd2

# replacing.. 

# ABORT: replacement failed. server out of range 
# attempting to reposition:

# Select option to replace: [1] nic card [2] heatsink [3] _hdd2

# Tray full, please replace




