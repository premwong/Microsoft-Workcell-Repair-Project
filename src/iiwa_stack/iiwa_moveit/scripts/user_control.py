#!/usr/bin/env python


##Author: Nano Premvuti
## University of Washington 
## Department of Electrical & Computer Engineering

import sys
import rospy
from iiwa_move_to_ee_pose import MoveGroupLeftArm

class ItemState(object):
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
	  move_group.goto_cartesian_state(0.4, 0.3, 0.3, 270)
	  rospy.sleep(1)
	  move_group.extend_trajectory(-0.06)
	  move_group._nic = False
	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return

def replace_heatsink(server, move_group):
	try:
		print "Press to start heatsink sequence"
		raw_input()
		move_group.goto_cartesian_state(0.1, 0.75, 0.2, 0, 'heatsink')
	except rospy.ROSInterruptException:
		return
	except KeyboardInterrupt:
		return

def main():
	try:
		server = ItemState(1, 'tray')
		myLeftArm = MoveGroupLeftArm()
		myLeftArm.load_component_list()
		# myLeftArm.goto_nic_position()
		myLeftArm.goto_cartesian_state(0.2, 0.6, 0.2, 270)


	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return

if __name__ == '__main__':
  main()





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




