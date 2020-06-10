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
from iiwa_msgs.srv import MoveConveyor
from config import * 

CONVEYOR_ENABLE = False
autostop_enable = True
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

def pick_nic(move_group):
	try:
		move_group.set_gripper(True)
		move_group.goto_component_position('nic')
		move_group.set_gripper(True)
		move_group.interpolated_trajectory(move_group.component_map['nic'].get_z_offset() - Z_OFFSET, 0.001)
		move_group.set_gripper(False)
		move_group.interpolated_trajectory(0.012, 0.002)
		move_group.goto_cartesian_state(-0.30, -0.55, 0.33, 0, 'nic_bin')
		# move_group.goto_cartesian_state(-0.30, -0.55, 0.20, 0, 'nic_bin')
		move_group.set_gripper(True)
		# move_group.goto_cartesian_state(-0.30, -0.55, 0.33, 0, 'nic_bin')
	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return

def place_nic(move_group):
	move_group.set_gripper(True)
	move_group.goto_cartesian_state(0.504, 0.173, 0.12, 0, 'nic', joint7_offset=270)
	rospy.sleep(0.3)
	move_group.goto_cartesian_state(0.504, 0.173, 0.092, 0, 'nic', joint7_offset=270)
	move_group.interpolated_trajectory(-0.012, 0.002)
	move_group.set_gripper(False)
	move_group.interpolated_trajectory(0.012, 0.002)
	move_group.goto_cartesian_state(0.504, 0.173, 0.13, 0, 'nic', joint7_offset=270)
	move_group.goto_component_position('nic', z_offset=0.14)
	move_group.goto_component_position('nic')
	move_group.interpolated_trajectory(-0.01, 0.002)
	move_group.set_gripper(True)
	move_group.goto_component_position('nic', z_offset=0.22)

def pick_heatsink(move_group):
	try:
		move_group.goto_component_position('heatsink1', z_offset=0.18)
		move_group.goto_component_position('heatsink1', z_offset=0.15)
		rospy.sleep(0.5)
		move_group.set_gripper(True)
		move_group.interpolated_trajectory(-.01, 0.002)
		move_group.set_gripper(False)
		move_group.interpolated_trajectory(.01, 0.002)
		move_group.goto_cartesian_state(0, -0.55, 0.30, 0, 'heatsink_bin')
		move_group.set_gripper(True)
	except rospy.ROSInterruptException:
		return
	except KeyboardInterrupt:
		return

def pick_hdd(move_group):
	global autostop_enable
	move_group.goto_component_position('hdd1', 0.20, joint7_offset=180)
	rospy.sleep(0.5)
	move_group.goto_component_position('hdd1', 0.134, joint7_offset=180)
	move_group.set_gripper(True)
	move_group.interpolated_trajectory(-.02, 0.001)
	move_group.set_gripper(False)
	move_group.interpolated_trajectory(.02, 0.001)
	move_group.goto_component_position('hdd1', 0.20, joint7_offset=180)
	move_group.goto_cartesian_state(0.25, -0.55, 0.30, 0, 'heatsink_bin', joint7_offset=180)
	move_group.set_gripper(True)
	# autostop_enable = False 
	move_conveyor("R")
	return True

def place_heatsink(move_group):
	# move_group.goto_cartesian_state(0.504, 0.145, 0.15, 0, 'nic', joint7_offset=90)
	move_group.set_gripper(True)
	move_group.goto_cartesian_state(0.63, 0.077, 0.21, 180, 'heatsink1')
	rospy.sleep(0.3)
	move_group.goto_cartesian_state(0.63, 0.077, 0.12, 180, 'heatsink1')
	move_group.interpolated_trajectory(-.01, 0.001)
	move_group.set_gripper(False)
	move_group.interpolated_trajectory(.01, 0.002)
	move_group.goto_cartesian_state(0.63, 0.077, 0.21, 180, 'heatsink1')
	move_group.goto_component_position('heatsink_place', z_offset=0.22)
	rospy.sleep(0.1)
	move_group.goto_component_position('heatsink_place', z_offset=0.15)
	move_group.interpolated_trajectory(-.01, 0.001)
	move_group.set_gripper(True)
	move_group.interpolated_trajectory(.01, 0.001)
	move_group.goto_component_position('heatsink_place', z_offset=0.22)

def test(move_group):
	# move_group.goto_cartesian_state(0.45, 0.6, 0.48, 0, 'ram', joint7_offset=0)
	move_group.set_gripper(True)
	move_group.goto_cartesian_state(0.33, 0.77, 0.43, 0, 'ram')
	move_group.goto_cartesian_state(0.14, 0.59, 0.43, 0, 'ram')
	move_group.goto_cartesian_state(0.14, 0.59, 0.20, 0, 'ram')
	# move_group.goto_component_position('ram', z_offset = 0.24)
	# move_group.goto_component_position('ram', z_offset = 0.22)
	move_group.interpolated_trajectory(-.012, 0.001)
	move_group.set_gripper(False)
	move_group.interpolated_trajectory(.012, 0.001)
	
	move_group.goto_cartesian_state(0.14, 0.6, 0.35, 0, 'ram')
	rospy.sleep(0.2)
	move_group.goto_cartesian_state(0.33, 0.77, 0.43, 0, 'ram')

def autostop_callback(camera_feed):
	global autostop_enable
	camera_feed_buffer = camera_feed.data
	# if camera_feed_buffer[6] <= 600 and autostop_enable:
	# 	move_conveyor("S")

def check_ik(move_group):
	failed_list = move_group.query_pose_and_check_ik()
	if failed_list == None:
		print '-------------all ik solutions found------------------------'
		return True
	else:
		print 'IK failed for:'
		print failed_list

# dispatch_table = {'nic':replace_nic, 'heatsink1':replace_heatsink1, 'heatsink2':replace_heatsink2, 'hdd1':replaceHddHandler_1, 'hdd2':replaceHddHandler_2}

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

def main():
	try:
		nic = Component('nic', NIC_OFFSET, HEATSINK_SEED_STATE, NIC_ROTATION, (0.6, 0, 0))
		nic_tray = Component('nic_tray', (0,0,0), NIC_SEED_STATE, NIC_ROTATION, (0.6, 0, 0), angle_offset=90)
		ram = Component('ram', RAM_OFFSET, RAM_SEED_STATE, RAM_ROTATION, (0.6, 0, 0))

		heatsink = Component('heatsink1', HEATSINK_OFFSET, HEATSINK_SEED_STATE, HEATSINK_ROTATION, (0.6, 0, 0), angle_offset=90)
		heatsink_place = Component('heatsink_place', HEATSINK_PLACE_OFFSET, HEATSINK_SEED_STATE, HEATSINK_ROTATION, (0.6,0,0), angle_offset=90)
		heatsink_bin = Component('heatsink_bin', HEATSINK_OFFSET, HEATSINK_BIN_SEED_STATE, HEATSINK_ROTATION, (0.6, 0, 0), angle_offset=0)
		hdd = Component('hdd1', HDD_OFFSET, HEATSINK_SEED_STATE, HEATSINK_ROTATION, (0.6, 0, 0), angle_offset=90)
		nic_bin = Component('nic_bin', NIC_OFFSET, NIC_BIN_SEED_STATE, NIC_ROTATION, (0.6, 0, 0))
		myLeftArm = MoveGroupLeftArm()
		myLeftArm.load_component_map([nic, heatsink, hdd, ram, nic_tray, nic_bin, heatsink_bin, heatsink_place])
		myLeftArm.print_state()
		test(myLeftArm)
		rospy.spin()

	except rospy.ROSInterruptException:
	  return
	except KeyboardInterrupt:
	  return

if __name__ == '__main__':
  main()
