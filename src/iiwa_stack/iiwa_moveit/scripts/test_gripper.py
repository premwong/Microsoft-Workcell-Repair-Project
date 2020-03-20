import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from iiwa_msgs.msg import WorkcellCartesian
from iiwa_msgs.msg import GripperState
from moveit_commander.conversions import pose_to_list
from iiwa_msgs.srv import *

def set_gripper(state):
  gripper_state = GripperState()
  gripper_state.open = state
  rate = rospy.Rate(100)
  gripper_io_publisher.publish(gripper_state)
  rate.sleep()
  gripper_io_publisher.publish(gripper_state)


gripper_io_publisher = rospy.Publisher('/command/GripperState', iiwa_msgs.msg.GripperState, queue_size=10)

rate_long = rospy.Rate(1)

def main():
  try:
    print " Press to test gripper..."
    raw_input()
    set_gripper(True)
    rate_long.sleep()
    set_gripper(False)
    rate_long.sleep()
    set_gripper(True)


    print "============ Python tutorial demo complete!"
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()