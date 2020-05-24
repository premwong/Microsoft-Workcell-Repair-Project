#!/usr/bin/env python
"""
@Author: Nano Premvuti @premwong
University of Washington 2020
Department of Electrical & Computer Engineering
"""
import sys
import rospy
from workcell_iiwa_control import MoveGroupLeftArm, Component
from std_msgs.msg import Float64MultiArray
from iiwa_msgs.srv import MoveConveyor, BluetoothFlag
from config import * 
from conveyor_client import *

CONVEYOR_ENABLE = False
bt_ready = False
conveyor_done = False
user_done = False
return_ready = False

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

	def __str__(self):
		parts_dict = get_parts_list()
		master_string = ""
		for part_name in parts_dict.keys():
			part_string = str(part_name) + ": " + str(parts_dict[part_name])
			master_string += part_string
		return master_string
			
def replace_nic(move_group):
	try:
		print "NIC selected. Press to start sequence"
		raw_input()
		move_group.set_gripper(True)
		move_group.goto_home_state()
		rospy.sleep(2)
		move_group.goto_component_position('nic')
		move_group.set_gripper(True)
		rospy.sleep(6)
		move_group.interpolated_trajectory(move_group.component_map['nic'].get_z_offset() - Z_OFFSET, 0.001)
		rospy.sleep(2)
		move_group.set_gripper(False)
		move_group.interpolated_trajectory(Z_OFFSET - move_group.component_map['nic'].get_z_offset(), 0.001)
		move_group.goto_home_state()
		move_group.set_gripper(True)
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

def test_replace(move_group):
	move_group.goto_home_state()
	rospy.sleep(6)
	move_group.goto_cartesian_state(0.1, 0.7, 0.25, 0, 'nic')
	rospy.sleep(3)
	move_group.interpolated_trajectory(-0.16, 0.001)

def autostop_callback(camera_feed):
	camera_feed_buffer = camera_feed.data

	if user_done:
		if camera_feed_buffer[6] <= 200:
			move_conveyor("S")
	else: 
		if camera_feed_buffer[6] >= 200:
			move_conveyor("S")
	
	conveyor_done = True

def check_ik(move_group):
	failed_list = move_group.query_pose_and_check_ik()
	if failed_list == None:
		print '-------------all ik solutions found------------------------'
		return True
	else:
		print 'IK failed for:'
		print failed_list

def bt_callback(command):
	if command.equals("start"):
		bt_ready = True
	if command.equals("returning server"):
		return_ready = True

def doneHandler():
	print("Finished repairing server.")
	user_done = True

def main():
	try:
		if CONVEYOR_ENABLE:
			rospy.Subscriber('camera_pose_feed', Float64MultiArray, autostop_callback)
			print 'waiting for conveyor service...'
			try:
				rospy.wait_for_service('move_conveyor', 1)
			except:
				print 'Service call timeout'
			try:
				move_conveyor = rospy.ServiceProxy('move_conveyor', MoveConveyor)
				print 'hello conveyor'
			except rospy.ServiceException as e:
				print(e)

		rospy.Subscriber("bt_ready", BluetoothFlag, bt_callback)
		user_done_pub = rospy.Publisher("user_done", String, queue_size=10)
		rate = rospy.Rate(10)

		TrayState = ItemState()
		dispatch_table = { 'nic':replace_nic, 
						   'heatsink1':replace_heatsink1, 
						   'heatsink2':replace_heatsink2, 
						   'hdd1':replaceHddHandler_1, 
						   'hdd2':replaceHddHandler_2.
						   'done':doneHandler }

		while not rospy.is_shutdown():
			if bt_ready:
				move_conveyor("F")
				if conveyor_done:
					while not user_done:
						print("Current Tray Status: ")
						print(str(TrayState))
						print("What part do you want to replace?")
						print("Type: nic, heatsink1, heatsink2, hdd1, hdd2, done")
						try:
							dispatch_table[input()]
						except KeyError:
							print("Invalid input, please type any of the following only: nic, heatsink1, heatsink2, hdd1, hdd2, done")
					# user is done, return the server when bt is ready
					if return_ready:
						move_conveyor("R")

					# reset flags to close up the cycle
					conveyor_done = False
					bt_ready = False
					return_ready = False
					
			rospy.spin()


		# nic = Component('nic', NIC_OFFSET, NIC_SEED_STATE, NIC_ROTATION, (0.6, 0, 0))
		# heatsink = Component('heatsink1', HEATSINK_OFFSET, NIC_SEED_STATE, HEATSINK_ROTATION, (0.6, 0, 0), angle_offset=90)
		# hdd = Component('hdd1', HEATSINK_OFFSET, NIC_SEED_STATE, HDD_ROTATION, (0.6, 0, 0), angle_offset=90)
		# myLeftArm = MoveGroupLeftArm()
		# myLeftArm.load_component_map([nic, heatsink, hdd])
		# myLeftArm.print_state()
		# test_replace(myLeftArm)

		# pose = myLeftArm.query_pose()
		# myLeftArm.check_ik_validity(pose)
		
		# # myLeftArm.goto_fiducial_position()
		# myLeftArm.goto_cartesian_state(0.1, 0.7, 0.25, -30, 'nic')
		# rospy.sleep(4)
		# # myLeftArm.execute_trajectory_from_file('nic_to_heatsink1')
		# # rospy.sleep(8)
		# myLeftArm.gotoartesian_state(0.0, 0.6, 0.25, 90, 'heatsink1')
		# move_conveyor("F")
		rospy.spin()

	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return

if __name__ == '__main__':
  main()
