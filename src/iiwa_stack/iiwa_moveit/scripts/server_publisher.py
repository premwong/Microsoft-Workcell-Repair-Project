#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
import geometry_msgs.msg
from iiwa_msgs.msg import WorkcellCartesian
from iiwa_msgs.msg import GripperState
def talker():
	pub = rospy.Publisher('server_pose_chatter', WorkcellCartesian, queue_size=10)
	pub = rospy.Publisher('command/GripperState', GripperState, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)
	state = GripperState()
	state.open = False
	print 'opening gripper'
	rospy.loginfo(state)
	pub.publish(state)
	rate.sleep()
	rospy.loginfo(state)
	pub.publish(state)
	rate.sleep()
	# rospy.init_node('talker', anonymous=True)
	# rate = rospy.Rate(0.1) #10Hz
	# while not rospy.is_shutdown():
	# 	pose_goal = WorkcellCartesian()
	# 	pose_goal.orientation_w = 1.57
	# 	pose_goal.orientation_x = 0
	# 	pose_goal.orientation_y = 0.71
	# 	pose_goal.orientation_z = 0
	# 	pose_goal.position_x = 0.28
	# 	pose_goal.position_y = 0.57
	# 	pose_goal.position_z = 1.17
	# 	rospy.loginfo(pose_goal)
	# 	pub.publish(pose_goal)
	# 	rate.sleep()
if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
	
