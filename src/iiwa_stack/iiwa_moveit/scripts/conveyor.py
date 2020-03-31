#! /usr/bin/env python
import rospy
import sys
import copy
from std_msgs.msg import String

rospy.init_node('conveyor_control', anonymous=True)
publisher = rospy.Publisher('conveyor', std_msgs.msg.String, queue_size=10)



