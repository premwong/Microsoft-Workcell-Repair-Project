#!/usr/bin/env python

import rospy
import sys
from iiwa_tool_moveit.srv import MoveConveyor

# This should come from the external bluetooth module
bl_ready = 1

def move_conveyor_client():
    rospy.wait_for_service('move_conveyor')
    try:
        move_conveyor = rospy.ServiceProxy('move_conveyor', MoveConveyor)
        if bl_ready == 1:
            move_conveyor("F")
        else:
            move_conveyor("R")
    except rospy.ServiceException as e:
        print(e)

if __name__ == "__main__":
    move_conveyor_client()