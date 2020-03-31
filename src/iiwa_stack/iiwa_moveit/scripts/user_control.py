#!/usr/bin/env python

import sys
import rospy
from iiwa_move_to_ee_pose import MoveGroupLeftArm

class ServerState(object):
	def __init__(self, server_id, type='server'):
		super(ServerState, self).__init__()
		if type == 'server':
			self._server_id = server_id
			self._heatsink1 = True
			self._heatsink2 = True
			self._nic = True
			self._hdd1 = True
			self._hdd2 = True
			self._dimm1 = True
			self._dimm2 = True


	def get_parts_list(self):
		return self.__dict__



def replace_nic(server, move_group):
	move_group.print_state()
	try:
	  print " Press to start sequence"
	  raw_input()
	  move_group.goto_cartesian_state(0.4, 0.3, 0.3, 270)
	  rospy.sleep(1)
	  move_group.extend_trajectory(-0.06)
	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return


def main():
	try:
		server = ServerState(1)
		print server.get_parts_list()
		myLeftArm = MoveGroupLeftArm()
		replace_nic(server, myLeftArm)


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




